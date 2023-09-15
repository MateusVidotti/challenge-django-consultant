from cpf_field.models import CPFField
from django.db import models
from django_extensions.db.models import TimeStampedModel
from utils.model_abstracts import Model
from django.forms import ModelForm
from loans.utils import FIELD_TYPES_CHOICES
from django.utils.module_loading import import_string


class Loan(Model, TimeStampedModel):
	"""Represents a loan request."""
	name = models.CharField(max_length=50)
	email = models.EmailField(verbose_name="Email")
	cpf = CPFField('cpf')
	value = models.FloatField(help_text='Value for loan')
	extra_infos = models.JSONField(null=True, blank=True)
	assess_by_api = models.BooleanField(default=False)
	approved_by_api = models.BooleanField(default=False)
	approved_by_admin = models.BooleanField(default=False)
	send_approved_email = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = "Loans"

	def __str__(self):
		return self.name


class LoanExtraField(models.Model):
	"""Represents extra fields for Laon form"""
	field_name = models.CharField(max_length=30)
	field_type = models.IntegerField(choices=FIELD_TYPES_CHOICES)
	field_attrs = models.JSONField(null=True, blank=True, help_text='Json with form fields attributes '
																	'ex.{"max_length": 30, "empty_value": ""}')


class LoanForm(ModelForm):
	"""Form to Laon plus LoanExtraField"""
	def __init__(self, *args, **kwargs):
		extra_fields = LoanExtraField.objects.all()
		super(LoanForm, self).__init__(*args, **kwargs)
		for field in extra_fields:
			if field.field_attrs is None:
				field.field_attrs = dict()
			self.fields[field.field_name] = import_string(f'django.forms.{field.get_field_type_display()}Field')\
				(**field.field_attrs)

	class Meta:
		model = Loan
		fields = ['name', 'email', 'cpf', 'value']
		labels = {'name': 'Nome', 'cpf': 'CPF', 'value': 'Valor'}
