from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.reverse import reverse

from loans.models import LoanForm
from loans.serializers import LoanSerializer
from loans.tasks import loan_assess


@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'loansrequest': reverse(
                'loansrequest', request=request, format=format
            ),
        }
    )


class LoansRequest(CreateModelMixin, GenericAPIView):
    """
    Create a new loan request.
    """

    serializer_class = LoanSerializer

    def get(self, request):
        form = LoanForm()
        form_settings = {'data': form.as_ul()}
        return Response(form_settings)

    def prepare_extra_data_to_serializer(self, request):
        extra_fields = dict()
        to_serializer = dict()
        s_fields = self.get_serializer().fields
        for data in request.data:
            if data in s_fields:
                to_serializer[data] = request.data[data]
            else:
                extra_fields[data] = request.data[data]
        to_serializer['extra_infos'] = extra_fields
        return to_serializer

    def post(self, request, *args, **kwargs):
        to_serializer = self.prepare_extra_data_to_serializer(request)
        serializer = self.get_serializer(data=to_serializer)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        loan_assess.delay(obj.id)   # send a request to api assess with celery
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
