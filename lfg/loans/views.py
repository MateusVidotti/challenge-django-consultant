from django.forms import modelform_factory
from loans.models import Loan
from loans.tasks import loan_assess
from loans.serializers import LoanSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class Loans(APIView):
    """
    List all loan requests
    """
    def get(self, request, format=None):
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)


class LoansRequest(APIView):
    """
    Create a new loan request.
    """
    def post(self, request):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            obj = serializer.save()
            loan_assess.delay(obj.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormSettings(APIView):
    """Get loan form settings."""
    def get(self, request, format=None):
        LoanForm = modelform_factory(Loan, exclude=['id', 'assess', 'approved_by_api', 'extra_values', 'created', 'modified'])
        form = LoanForm()
        form_settings = {'data': form.as_ul()}
        # return Response(JSONRenderer().render(form_settings))
        return Response(form_settings)
