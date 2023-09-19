from django.contrib import admin

from loans.models import Loan, LoanExtraField


def approve_loans(modeladmin, request, queryset):
    """Approve only loans already approved by api"""
    for obj in queryset:
        if obj.approved_by_api:
            obj.approved_by_admin = True
            obj.save()


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'assess_by_api',
        'approved_by_api',
        'approved_by_admin',
    )
    readonly_fields = ('approved_by_api', 'assess_by_api', 'approved_by_admin')
    list_filter = ('approved_by_api',)
    actions = [approve_loans]


@admin.register(LoanExtraField)
class LoanExtraFieldAdmin(admin.ModelAdmin):
    list_display = ('field_name',)
