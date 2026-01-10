from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from django.conf import settings
from architect_app.models import Architect, ClientProfile, Contract, Project
from seller_app.models import Seller  # ajuste se o app for outro

#para rodar: python manage.py populate_architects
#https://chatgpt.com/c/6961ecec-8f48-8326-ac16-cccd4f315b1b


class Command(BaseCommand):
    help = "Popula o banco com 3 arquitetos, 4 contratos e 4 projetos cada"

    def handle(self, *args, **kwargs):
        self.stdout.write("🔧 Populando banco de dados...")

        today = timezone.now().date()

        for a in range(1, 4):
            # ===== USER / SELLER =====
            seller = Seller.objects.create_user(
                username=f"architect{a}",
                email=f"architect{a}@example.com",
                password="123456"
            )

            # ===== ARCHITECT PROFILE =====
            architect = Architect.objects.create(
                user=seller,
                firm_name=f"Architect Studio {a}",
                license_number=f"LIC-{a:03}",
                phone_number=f"1199999000{a}"
            )

            # ===== CLIENT PROFILE (1 client per architect) =====
            client_user = Seller.objects.create_user(
                username=f"client{a}",
                email=f"client{a}@example.com",
                password="123456"
            )

            client = ClientProfile.objects.create(
                user=client_user,
                architect=architect,
                company_name=f"Client Company {a}",
                phone_number=f"1188888000{a}"
            )

            # ===== CONTRACTS =====
            for c in range(1, 5):
                contract = Contract.objects.create(
                    architect=architect,
                    client=client,
                    title=f"Contract {a}.{c}",
                    start_date=today,
                    end_date=today + timedelta(days=180),
                    is_active=True,
                    budget=100000 * c
                )

                # ===== PROJECTS =====
                for p in range(1, 5):
                    Project.objects.create(
                        contract=contract,
                        name=f"Project {a}.{c}.{p}",
                        description="Projeto arquitetônico",
                        location="São Paulo",
                        expected_completion_date=today + timedelta(days=90 + p * 10),
                        completion_date=None
                    )

        self.stdout.write(self.style.SUCCESS("✅ Banco populado com sucesso!"))
