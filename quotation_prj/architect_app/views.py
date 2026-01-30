from time import timezone
from django.utils import timezone
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.db import transaction
from .models import Architect, Contract, Project, ClientProfile
from .forms import ArchitectUnifiedSettingsForm, ContractForm, SellerSignUpForm, ClientSignUpForm, ProjectForm, ClientEditForm, ArchitectSettingsForm
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib import messages


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
@role_required(allowed_roles=['CLIENT', 'OPERATOR'])
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
        # Re-apply the filter on POST to prevent cross-architect ID manipulation
        form.fields['client'].queryset = ClientProfile.objects.filter(architect=architect) 
        
        if form.is_valid():
            new_contract = form.save(commit=False)
            new_contract.architect = architect  # Explicitly link to current architect
            new_contract.save()
            return redirect('architects_contracts')
    else:
        form = ContractForm(instance=contract)
        # Filter the dropdown to only show clients belonging to this architect
        form.fields['client'].queryset = ClientProfile.objects.filter(architect=architect)
    
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

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        # Assumes your User model has a 'role' attribute
        return self.request.user.role in self.allowed_roles

class ProjectDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    allowed_roles = ['ARCHITECT', 'OPERATOR']
    model = Project
    template_name = 'architect_app/project_detail.html'
    context_object_name = 'project'

class ProjectUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ['ARCHITECT', 'OPERATOR']
    model = Project
    form_class = ProjectForm
    template_name = 'architect_app/project_edit.html'
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})
    
@login_required
@role_required(allowed_roles=['ARCHITECT', 'OPERATOR'])
def project_upsert(request, pk=None):
    """Handles both Creating and Editing a project."""
    project = get_object_or_404(Project, pk=pk) if pk else None
    architect = get_object_or_404(Architect, user=request.user)
    constract_queryset = Contract.objects.filter(architect=architect)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            # The contract is already selected in the form, 
            # and because we filter the queryset below, it's safe.
            new_project = form.save()
            return redirect('architects_projects')
    else:
        form = ProjectForm(instance=project)
        # Filter the contract dropdown to only show contracts belonging to this architect
        form.fields['contract'].queryset = constract_queryset
    
    return render(request, 'architect_app/project_edit.html', {
        'form': form, 
        'project': project
    })

class ProjectDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    allowed_roles = ['ARCHITECT']
    model = Project
    template_name = 'architect_app/project_confirm_delete.html'
    success_url = reverse_lazy('architects_projects')

    def get_queryset(self):
        """Ensure an architect can only delete projects from their own contracts."""
        return self.model.objects.filter(contract__architect__user=self.request.user)
    
User = get_user_model()

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

@login_required
@role_required(allowed_roles=['ARCHITECT'])
def client_invite(request):
    architect = get_object_or_404(Architect, user=request.user)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')

        # Check if a user with this email already exists
        existing_user = User.objects.filter(email=email).first()
        
        if existing_user:
            # Check if this user is already registered as a client (with any architect)
            if ClientProfile.objects.filter(user=existing_user).exists():
                messages.error(request, "Client with this email already exists." \
                " If you want to link this client to your architect account, please contact support on wiserarch@gmail.co.")
                return redirect('architects_clients')
        
        with transaction.atomic():
            # 1. Get or Create the User
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,
                    'first_name': first_name,
                    'role': 'CLIENT',
                    'is_active': True 
                }
            )
            
            # 2. Create/Link the Profile
            ClientProfile.objects.update_or_create(
                user=user,
                defaults={'architect': architect}
            )

            # 3. MANUAL EMAIL LOGIC (Bypasses PasswordResetForm filters)
            context = {
                'email': user.email,
                'domain': request.get_host(), # Will be 127.0.0.1:8000 in dev
                'site_name': 'Architect Portal',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',
                'architect': architect,
            }

            subject = _("Invitation to join %(firm)s Portal") % {'firm': architect.firm_name}
            # Make sure this template exists in templates/registration/invite_email.html
            body = render_to_string('registration/invite_email.html', context)

            # This will show up in your terminal immediately
            send_mail(
                subject,
                body,
                'noreply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )

            # Add the success message here
            messages.success(request, f'Success! An invitation email has been sent to {email}.')

        return redirect('architects_clients')
    
    return render(request, 'architect_app/client_invite_form.html')


@login_required
@role_required(allowed_roles=['ARCHITECT'])
def client_edit(request, pk):
    # Ensure the architect can only edit THEIR clients
    architect = get_object_or_404(Architect, user=request.user)
    client_profile = get_object_or_404(ClientProfile, pk=pk, architect=architect)

    if request.method == 'POST':
        form = ClientEditForm(request.POST, instance=client_profile)
        if form.is_valid():
            form.save()
            return redirect('architects_clients')
    else:
        form = ClientEditForm(instance=client_profile)

    return render(request, 'architect_app/client_form.html', {
        'form': form,
        'client': client_profile
    })

@login_required
@role_required(allowed_roles=['ARCHITECT'])
def client_delete(request, pk):
    # Ensure the architect can only delete THEIR clients
    architect = get_object_or_404(Architect, user=request.user)
    client_profile = get_object_or_404(ClientProfile, pk=pk, architect=architect)
    
    if request.method == 'POST':
        # This will cascade and delete related Contracts and Projects
        # It will NOT delete the actual User object unless you explicitly do so
        user = client_profile.user
        client_profile.delete()
        # Optional: delete the user account as well if they shouldn't exist without a profile
        # user.delete() 
        
        messages.success(request, "Client and all associated data deleted successfully.")
        return redirect('architects_clients')
    
    return render(request, 'architect_app/client_confirm_delete.html', {
        'client': client_profile
    })

@login_required
@role_required(allowed_roles=['ARCHITECT'])
def client_reinvite(request, pk):
    architect = get_object_or_404(Architect, user=request.user)
    # Ensure this client belongs to the requesting architect
    client_profile = get_object_or_404(ClientProfile, pk=pk, architect=architect)
    user = client_profile.user

    # MANUAL EMAIL LOGIC (Consistent with your client_invite logic)
    context = {
        'email': user.email,
        'domain': request.get_host(),
        'site_name': 'Architect Portal',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': default_token_generator.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
        'architect': architect,
    }

    subject = _("Re-invitation to join %(firm)s Portal") % {'firm': architect.firm_name}
    body = render_to_string('registration/invite_email.html', context)

    send_mail(
        subject,
        body,
        'noreply@yourdomain.com',
        [user.email],
        fail_silently=False,
    )

    messages.success(request, f'Re-invitation sent successfully to {user.email}.')
    return redirect('architects_clients')

@login_required
@role_required(allowed_roles=['ARCHITECT'])
def architect_settings(request):
    architect = get_object_or_404(Architect, user=request.user)
    
    if request.method == 'POST':
        form = ArchitectUnifiedSettingsForm(request.POST, request.FILES, instance=architect)
        if form.is_valid():
            form.save()
            messages.success(request, "All settings updated successfully.")
            return redirect('architect_settings')
    else:
        form = ArchitectUnifiedSettingsForm(instance=architect)
        
    return render(request, 'architect_app/architect_settings.html', {'form': form, 'architect': architect})