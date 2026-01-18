from time import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Architect, Contract, Project, ClientProfile
from .forms import ContractForm, SellerSignUpForm, ClientSignUpForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to the dispatcher we created earlier
            return redirect('dashboard_redirect') 
    else:
        form = SellerSignUpForm()
    return render(request, 'registration/signup3roles.html', {'form': form})

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator

@login_required
def dashboard_redirect(request):
    """
    Acts as the dynamic LOGIN_REDIRECT_URL logic.
    """
    user = request.user
    print("dashboard_redirect for user:", user.username, "with role:", user.role)
    # Logic based on the 'role' field we added to the Seller model
    if user.role == 'ARCHITECT':
        return redirect('architect_dashboard')
    elif user.role == 'CLIENT':
        return redirect('client_dashboard')
    elif user.role == 'OPERATOR':
        return redirect('operator_dashboard')
    
    # Fallback for users without a specific role assigned
    return redirect('login')

def client_signup_view(request):
    # Assume the URL is /signup/client/?arch=1
    architect_id = request.GET.get('arch') 
    
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Get the architect instance
            try:
                architect = Architect.objects.get(id=request.POST.get('architect_id'))
                # Create the profile and link it to the architect
                ClientProfile.objects.create(user=user, architect=architect)
            except Architect.DoesNotExist:
                # Handle error: Every client must have an architect
                pass
                
            login(request, user)
            return redirect('client-portal')
    else:
        form = ClientSignUpForm(initial={'architect_id': architect_id})
        
    return render(request, 'registration/signup_client.html', {'form': form})

@login_required
@role_required(allowed_roles=['ARCHITECT', 'OPERATOR'])
def architect_dashboard(request):
    architect = get_object_or_404(Architect, user=request.user)

    clients_count = architect.clients.count()
    active_contracts = architect.contracts.filter(is_active=True)
    active_contracts_count = active_contracts.count()

    total_budget = active_contracts.aggregate(
        total=Sum('budget')
    )['total'] or 0

    projects_count = Project.objects.filter(
        contract__architect=architect
    ).count()

    recent_contracts = architect.contracts.select_related(
        'client__user'
    ).order_by('-start_date')[:5]

    recent_projects = Project.objects.filter(
        contract__architect=architect
    ).select_related('contract').order_by('-expected_completion_date')[:5]

    context = {
        'architect': architect,
        'clients_count': clients_count,
        'active_contracts_count': active_contracts_count,
        'total_budget': total_budget,
        'projects_count': projects_count,
        'recent_contracts': recent_contracts,
        'recent_projects': recent_projects,
    }

    return render(request, 'architect_app/dashboard.html', context)

@login_required
@role_required(allowed_roles=['ARCHITECT', 'OPERATOR'])
def project_list(request):
    architect = get_object_or_404(Architect, user=request.user)
    
    # Get all contracts for the architect to populate the filter dropdown
    contracts = Contract.objects.filter(architect=architect)
    
    # Start with all projects belonging to this architect
    projects = Project.objects.filter(contract__architect=architect)
    
    # Apply filter if a specific contract is selected
    selected_contract_id = request.GET.get('contract')
    if selected_contract_id:
        projects = projects.filter(contract_id=selected_contract_id)

    context = {
        'projects': projects,
        'contracts': contracts,
        'selected_contract_id': selected_contract_id,
    }
    return render(request, 'architect_app/projects.html', context)

@login_required
@role_required(allowed_roles=['ARCHITECT'])
def client_list(request):
    # Fetch clients directly linked to this architect
    architect = get_object_or_404(Architect, user=request.user)
    clients = architect.clients.all()
    return render(request, 'architect_app/archClients.html', {'clients': clients})

@login_required
@role_required(allowed_roles=['ARCHITECT'])
def contract_list(request):
    # Fetch all contracts for this architect
    architect = get_object_or_404(Architect, user=request.user)
    contracts = architect.contracts.all().select_related('client__user')
    return render(request, 'architect_app/contracts.html', {'contracts': contracts})

@login_required
@role_required(allowed_roles=['ClIENT', 'OPERATOR'])
def client_dashboard(request):
    # 1. Get the profile for the logged-in client
    # We use select_related('architect') to fetch the architect's data in the same query
    client = get_object_or_404(ClientProfile.objects.select_related('architect__user'), user=request.user)
    
    # 2. Get the Architect associated with this client
    architect = client.architect
    
    # 3. Fetch all contracts belonging to this client
    contracts = client.contracts.all()
    
    # 4. Fetch projects linked to this client
    # We filter by client directly since Project -> Contract -> Client
    projects = Project.objects.filter(contract__client=client).select_related('contract')
    
    context = {
        'client': client,
        'architect': architect,
        'contracts': contracts,
        'projects': projects,
    }
    print("contracts.progress_percentage: ", contracts.values('progress_percentage').all())
    return render(request, 'architect_app/client_dashboard.html', context)

# Helper function to add a message to a project's conversation log
def add_message(request, project_id):
    project = Project.objects.get(id=project_id)
    new_entry = {
        "sender": request.user.username,
        "message": request.POST.get('message'),
        "timestamp": str(timezone.now())
    }
    project.conversation_log.append(new_entry)
    project.save()

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from .models import Project

# better add message function, This view uses transaction.atomic to ensure that if two people post at the exact same microsecond, the data remains consistent.
# TODO test both
@login_required
@role_required(allowed_roles=['ARCHITECT', 'CLIENT'])
def add_project_message(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)
        message = request.POST.get('message', '').strip()

        if message:
            # Atomic ensures database integrity during the update
            with transaction.atomic():
                # Create the log entry
                new_entry = {
                    "user": request.user.get_full_name() or request.user.username,
                    "role": "Architect" if request.user.is_staff else "Client",
                    "text": message[:280], # Enforce limit
                    "timestamp": timezone.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Append to JSON log
                if not project.conversation_log:
                    project.conversation_log = []
                project.conversation_log.append(new_entry)

                # Update the specific Twitter-length field based on who sent it
                if request.user.is_staff: # Assuming Architect is staff
                    project.architect_comments = message[:280]
                else:
                    project.client_comments = message[:280]

                project.save()

        return redirect('project_detail', project_id=project.id)
    
@login_required
@role_required(allowed_roles=['ARCHITECT'])
def contract_upsert(request, pk=None):
    """Handles both Creating and Editing a contract."""
    contract = get_object_or_404(Contract, pk=pk) if pk else None
    architect = get_object_or_404(Architect, user=request.user)

    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            new_contract = form.save(commit=False)
            new_contract.architect = architect  # Link to current architect
            new_contract.save()
            return redirect('architects_contracts')
    else:
        form = ContractForm(instance=contract)
    
    return render(request, 'architect_app/contract_form.html', {'form': form, 'contract': contract})

@login_required
@role_required(allowed_roles=['ARCHITECT'])
def contract_delete(request, pk):
    contract = get_object_or_404(Contract, pk=pk, architect__user=request.user)
    if request.method == 'POST':
        contract.delete()
        return redirect('architects_contracts')
    return render(request, 'architect_app/contract_confirm_delete.html', {'contract': contract})

@login_required
@role_required(allowed_roles=['OPERATOR'])
def operator_dashboard(request):
    return render(request, 'architect_app/operator_dashboard.html')