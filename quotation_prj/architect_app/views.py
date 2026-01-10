from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Architect, Contract, Project, ClientProfile


@login_required
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
