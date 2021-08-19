from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator

from .validators import validate_starts_with_zero


class Account(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='account',
    )
    inn = models.CharField(
        'ИНН', 
        max_length=11,
        validators=[validate_starts_with_zero,],
        unique=True,
    )
    balance = models.DecimalField(
        'баланс',
        max_digits=2,
    )


class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(
        User,
        verbose_name='отправитель',
        related_name='transactions_sent',
        on_delete=models.DO_NOTHING,
    )
    receiver = models.ForeignKey(
        User,
        verbose_name='получатель',
        related_name='transactions_receieved',
        on_delete=models.DO_NOTHING,
    )
    amount = models.DecimalField(
        'сумма',
        max_digits=2,
    )
