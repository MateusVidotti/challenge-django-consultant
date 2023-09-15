from rest_framework import serializers
from loans.models import Loan


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = ['name', 'email', 'cpf', 'value', 'extra_infos']
