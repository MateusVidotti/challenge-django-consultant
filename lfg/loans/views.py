from django.forms import modelform_factory
from loans.models import Loan
from loans.serializers import LoanSerializer
from loans.tasks import loan_assess
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class Loans(ListModelMixin, GenericAPIView):
    """
    List all loan requests
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class LoansRequest(CreateModelMixin, GenericAPIView):
    """
    Create a new loan request.
    """
    serializer_class = LoanSerializer

    def get(self, request, format=None):
        LoanForm = modelform_factory(Loan, labels={'name': 'Nome', 'cpf': 'CPF', 'value': 'Valor'},
                                     exclude=['id', 'assess', 'approved_by_api', 'extra_values', 'created', 'modified'])
        form = LoanForm()
        form_settings = {'data': form.as_ul()}
        return Response(form_settings)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        obj = serializer.save()
        loan_assess.delay(obj.id)


class FormSettings(APIView):
    """Get loan form settings."""
    def get(self, request, format=None):
        LoanForm = modelform_factory(Loan, labels={'name': 'Nome', 'cpf': 'CPF', 'value': 'Valor'},
                                     exclude=['id', 'assess', 'approved_by_api', 'extra_values', 'created', 'modified'])
        form = LoanForm()
        form_settings = {'data': form.as_ul()}
        return Response(form_settings)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'api/loans': reverse('loans', request=request, format=format),
        'loansrequest': reverse('loansrequest', request=request, format=format),
        'formsettings': reverse('formsettings', request=request, format=format)
    })
