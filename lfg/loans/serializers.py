from loans.models import Loan
from rest_framework import serializers


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['name', 'email', 'cpf', 'value', 'extra_infos']
