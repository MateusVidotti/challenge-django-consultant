from cpf_field.models import CPFField
from django.db import models
from django_extensions.db.models import TimeStampedModel
from utils.model_abstracts import Model


class Loan(Model, TimeStampedModel):
	"""Represents a loan request."""
	name = models.CharField(max_length=50)
	email = models.EmailField(verbose_name="Email")
	cpf = CPFField('cpf')
	rg = models.CharField(max_length=10, default='')
	address = models.CharField(max_length=50, default='')
	value = models.FloatField(help_text='Value for loan')
	assess_by_api = models.BooleanField(default=False)
	approved_by_api = models.BooleanField(default=False)
	approved_by_admin = models.BooleanField(default=False)
	send_approved_email = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = "Loans"

	def __str__(self):
		return self.name


class LoanExcluedField(models.Model):
	"""Represents fields from Laon to exclude from form"""
	field_name = models.CharField(max_length=10)
