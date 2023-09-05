from django.contrib import admin
from loans.models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('name', 'assess', 'approved_by_api')
    readonly_fields = ('approved_by_api', 'assess')
