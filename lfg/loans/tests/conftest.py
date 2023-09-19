import pytest
from rest_framework.test import APIClient

from loans.models import Loan


@pytest.fixture
def api_client():
    return APIClient
