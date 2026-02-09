from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from django.conf import settings
from architect_app.models import Architect, ClientProfile, Contract, Project, Operator
from seller_app.models import Seller  # ajuste se o app for outro

#para rodar: python manage.py populate_architects
#https://chatgpt.com/c/6961ecec-8f48-8326-ac16-cccd4f315b1b


class Command(BaseCommand):
    help = "Populates the database with Architects, Clients, Operators, Contracts, and Projects"

    def handle(self, *args, **kwargs):
        self.stdout.write("🔧 Populando banco de dados com novos perfis de acesso...")

        today = timezone.now().date()

        # 1. Create the 1st user: wa_user
        # Using get_or_create prevents duplicates if you run the script twice
        wa_user, created = Seller.objects.get_or_create(
            username="wa_user",
            email="wiserarch@gmail.com",    
            defaults={'role': Seller.Roles.ARCHITECT}
        )
        if created:
            wa_user.set_password("123456")
            wa_user.save()

        # 1.1. CREATE OPERATOR
        op_user, created = Seller.objects.get_or_create(
            username="admin_operator",
            email="operator@portal.com",
            defaults={'role': Seller.Roles.OPERATOR}
        )
        if created:
            op_user.set_password("123456")
            op_user.save()
            # The signal likely created the Operator profile, let's update it
            operator_profile = Operator.objects.get(user=op_user)
            operator_profile.department = "System Admin"
            operator_profile.save()
            self.stdout.write(f"Created Operator: {op_user.username}")

        # 2. CREATE ARCHITECTS, CLIENTS, AND PROJECTS
        for a in range(1, 4):
            # ===== SELLER (ARCHITECT ROLE) =====
            arch_user, created = Seller.objects.get_or_create(
                username=f"architect{a}",
                email=f"architect{a}@example.com",
                defaults={'role': Seller.Roles.ARCHITECT}
            )
            if created:
                arch_user.set_password("123456")
                arch_user.save()

            # ===== ARCHITECT PROFILE =====
            # Use update_or_create in case the signal already made the profile
            architect, _ = Architect.objects.update_or_create(
                user=arch_user,
                defaults={
                    'firm_name': f"Architect Studio {a}",
                    'license_number': f"LIC-{a:03}",
                    'phone_number': f"1199999000{a}"
                }
            )

            # ===== SELLER (CLIENT ROLE) =====
            client_user, created = Seller.objects.get_or_create(
                username=f"client{a}",
                email=f"client{a}@example.com",
                defaults={'role': Seller.Roles.CLIENT}
            )
            if created:
                client_user.set_password("123456")
                client_user.save()

            # ===== CLIENT PROFILE =====
            # IMPORTANT: Signals skip ClientProfile creation because of the 'architect' FK requirement
            client, _ = ClientProfile.objects.get_or_create(
                user=client_user,
                architect=architect, # Link to current architect
                defaults={
                    'company_name': f"Client Company {a}",
                    'phone_number': f"1188888000{a}"
                }
            )

            # ===== CONTRACTS =====
            for c in range(1, 3): # Reduced to 2 contracts for brevity
                contract, _ = Contract.objects.get_or_create(
                    architect=architect,
                    client=client,
                    title=f"Contract {a}.{c}",
                    defaults={
                        'start_date': today,
                        'end_date': today + timedelta(days=180),
                        'is_active': True,
                        'budget': 100000 * c
                    }
                )

                # ===== PROJECTS =====
                for p in range(1, 3):
                    Project.objects.get_or_create(
                        contract=contract,
                        name=f"Project {a}.{c}.{p}",
                        defaults={
                            'description': "Projeto arquitetônico gerado automaticamente",
                            'location': "São Paulo, SP",
                            'expected_completion_date': today + timedelta(days=90 + p * 10)
                        }
                    )

        self.stdout.write(self.style.SUCCESS("✅ Banco populado com sucesso!"))