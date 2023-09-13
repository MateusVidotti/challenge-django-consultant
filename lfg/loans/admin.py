from django.contrib import admin
from loans.models import Loan, LoanExcluedField


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('name', 'assess_by_api', 'approved_by_api', 'approved_by_admin')
    readonly_fields = ('approved_by_api', 'assess_by_api')


@admin.register(LoanExcluedField)
class LoanExcluedFieldAdmin(admin.ModelAdmin):
    list_display = ('field_name',)
