import requests
from celery import shared_task
from django.core.mail import send_mail

from loans.models import Loan


@shared_task
def send_fail_mail(loan_id):
    """Send mail for not accepted loan."""
    loan_request = Loan.objects.get(id=loan_id)
    send_mail(
        'Pedido recusado',
        'O seu pedido de empréstimo foi recusado. Tente mais uma vez',
        'support@example.com',
        (loan_request.email,),
        fail_silently=False,
    )


@shared_task
def send_sucess_mail(loan_id):
    """Send mail for accepted loan."""
    loan_request = Loan.objects.get(id=loan_id)
    send_mail(
        'Pedido Aprovado',
        f'O seu pedido de empréstimo foi aprovado. O valor de {loan_request.value} já está disponível',
        'support@example.com',
        (loan_request.email,),
        fail_silently=False,
    )


@shared_task
def loan_assess(loan_id):
    """Assess a loan with digitalsys api"""
    loan_request = Loan.objects.get(id=loan_id)
    api_url = 'https://loan-processor.digitalsys.com.br/api/v1/loan'
    data = {
        'name': loan_request.name,
        'document': {'email': loan_request.email, 'cpf': loan_request.cpf},
    }
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        loan_request.assess_by_api = True
        if response.json()['approved'] is True:
            loan_request.approved_by_api = True
        else:
            loan_request.approved_by_api = False
            send_fail_mail.delay(loan_id)
        loan_request.save()
    return response
