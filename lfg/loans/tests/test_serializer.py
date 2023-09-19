import pytest
from loans.models import Loan
from loans.serializers import LoanSerializer

pytestmark = pytest.mark.django_db


class TestLoanSerializer:
    def test_serializer_model(self):
        serializer = LoanSerializer(Loan())
        assert serializer

    def test_serializer_data(self):
        loan = Loan(
            name='Paulo do django',
            cpf='33575854807',
            email='paulo@django.com',
            value=1000,
        )
        serializer = LoanSerializer(loan)
        data_expected = {
            'name': 'Paulo do django',
            'email': 'paulo@django.com',
            'cpf': '33575854807',
            'value': 1000.0,
            'extra_infos': None,
        }
        assert serializer.data == data_expected

    def test_deserializer_data(self):
        serializer = LoanSerializer(
            data={
                'name': 'Paulo do django',
                'email': 'paulo@django.com',
                'cpf': '33575854807',
                'value': 1000.0,
                'extra_infos': None,
            }
        )
        assert serializer.is_valid()
