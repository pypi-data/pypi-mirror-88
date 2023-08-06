import json
import math

from datetime import datetime

from django.db import models

class BasePlan(models.Model):
    PLAN_ACCESS_TIME_CHOICES = (
        ('FULL_ACCESS', 'Acesso completo'),
        ('FREE_TRIAL', 'Teste gratuito')
    )
    name = models.CharField(max_length=100)
    plan_access_time = models.CharField(max_length=20, choices=PLAN_ACCESS_TIME_CHOICES, default='FREE_TRIAL')
    description = models.TextField(null=True, blank=True)
    base_price = models.FloatField(default=0.0)
    free_trial_days = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)
    auto_payment = models.BooleanField(default=False)
    has_quota_expansion = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s - %s' % (self.name, self.get_plan_access_time_display())

    def get_plan_duration(self):
        if self.plan_access_time == 'FULL_ACCESS':
            return None
        elif self.plan_access_time == 'FREE_TRIAL':
            return self.free_trial_days

    def is_expired(self):
        if self.get_days_remaining() < 0:
            return True
        return False

class BaseBillingInfo(models.Model):
    credit_card_id = models.CharField(max_length=50, null=True, blank=True)
    last_four_card_number = models.CharField(max_length=4, null=True, blank=True)
    expiration_month = models.PositiveSmallIntegerField(null=True, blank=True)
    expiration_year = models.PositiveSmallIntegerField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    document = models.CharField(max_length=14, null=True, blank=True)
    email = models.CharField(max_length=320, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    street = models.CharField(max_length=256, null=True, blank=True)
    avenue = models.CharField(max_length=256, null=True, blank=True)
    number = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    postcode = models.CharField(max_length=256,  null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.company.name


class BasePaymentRecord(models.Model):
    STATUS_CHOICES = (
        ('PAID', 'Pago'),
        ('NOT_PAID', 'Não pago'),
        ('CANCELED', 'Cancelado')
    )
    TYPE_CHOICES = (
        ('MONTHLY_PAYMENT', 'Pagamento mensal'),
        ('EXPANSION_REQUEST', 'Solicitação de expansão de quota')
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='NOT_PAID')
    payment_type = models.CharField(max_length=17, choices=TYPE_CHOICES, default='MONTHLY_PAYMENT')
    amount = models.FloatField(default=0.0)
    charge_id = models.CharField(max_length=100, null=True, blank=True)
    amount_quota_expansion = models.IntegerField(default=0, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.company.name


class BasePlanRelation(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Ativo'),
        ('NOT_PAID', 'Não pago'),
        ('CANCELED', 'Cancelado')
    )
    start_date = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    credits = models.FloatField(default=0.0)

    class Meta:
        abstract = True

class BaseQuota(models.Model):
    quota_type = models.CharField(max_length=100)
    price_per_item = models.FloatField(default=0.0)
    num_items = models.IntegerField(default=0)

    class Meta:
        abstract = True

    def get_total_price(self):
        return self.num_items * self.price_per_item
