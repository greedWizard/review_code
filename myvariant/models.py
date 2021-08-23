from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator


class Account(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='account',
    )
    inn = models.CharField(
        'ИНН', 
        unique=True,
    )
    balance = models.DecimalField(
        'баланс',
        decimal_places=2,
        default=0.0,
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
