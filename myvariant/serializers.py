from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Account, Transaction
from users.serializers import UserSerializer


class TransactionSerializerBase(ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'amount',
        ]


class TransactionSerializerRead(TransactionSerializerBase):
    sender = UserSerializer(many=False)
    receiver = UserSerializer(many=False)

    class Meta(TransactionSerializerBase.Meta):
        fields = TransactionSerializerBase.Meta.fields + [
            'id', 'sender', 'receiver',
        ]


class TransactionSerializerPost(TransactionSerializerBase):
    inn_to = serializers.ListField(
        children=serializers.CharField()
    )
    sender_id = serializers.IntegerField()

    class Meta(TransactionSerializerBase.Meta):
        fields = TransactionSerializerBase.Meta.fields + [
            'inn_to', 'sender_id',
        ]
