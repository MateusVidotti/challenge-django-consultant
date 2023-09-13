from django.forms import modelform_factory
from loans.models import Loan, LoanExcluedField
from loans.serializers import LoanSerializer
from loans.tasks import loan_assess
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'loansrequest': reverse('loansrequest', request=request, format=format),
    })


class LoansRequest(CreateModelMixin, GenericAPIView):
    """
    Create a new loan request.
    """
    serializer_class = LoanSerializer

    def get(self, request, format=None):
        excluded_felds = ['id', 'assess_by_api', 'approved_by_api', 'extra_values', 'created', 'modified',
                          'send_approved_email', 'approved_by_admin']
        fields = LoanExcluedField.objects.all()
        for field in fields:
            excluded_felds.append(field.field_name)
        LoanForm = modelform_factory(Loan,  labels={'name': 'Nome', 'cpf': 'CPF', 'rg': 'RG', 'address': 'Endereço',
                                                    'value': 'Valor'},
                                     exclude=excluded_felds)
        form = LoanForm()
        form_settings = {'data': form.as_ul()}
        return Response(form_settings)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        obj = serializer.save()
        loan_assess.delay(obj.id)
