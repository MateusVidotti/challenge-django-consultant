import json
import pytest
from rest_framework.reverse import reverse
from loans.models import LoanForm, Loan
import re
from model_bakery import baker

pytestmark = pytest.mark.django_db


class TestLoanRequestEndpoint:
    endpoint = reverse('loansrequest')

    def test_list_fields(self, api_client):
        response = api_client().get(self.endpoint)
        form = LoanForm()
        n_formfields = len(form.fields)
        assert len(re.compile('input').findall(json.loads(response.content)['data'])) == n_formfields

    def test_post_loanrequest(self, api_client):
        json_post = {
            "cpf": "33575854807",
            "email": "ze@django.com",
            "name": "Zé do Django",
            "value": 1000,
        }
        response = api_client().post(
            self.endpoint,
            data=json_post,
            format='json'
        )
        assert response.status_code == 201

    def test_post_loanrequest_with_extra_infos(self, api_client):
        json_post = {
            "cpf": "33575854807",
            "email": "ze@django.com",
            "name": "Zé do Django",
            "value": 1000,
            "rg": '87.888.888-48',
            "nacionalidade": "Brasileiro"
        }
        response = api_client().post(
            self.endpoint,
            data=json_post,
            format='json'
        )
        loan = Loan.objects.first()
        assert loan.extra_infos == {"rg": '87.888.888-48', "nacionalidade": "Brasileiro"}



