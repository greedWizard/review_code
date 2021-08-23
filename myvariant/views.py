from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .services import TransactionService
from .serializers import TransactionSerializerPost, TransactionSerializerRead


class TransactionViewSet(ViewSet):
    service = TransactionService
    read_serializer = TransactionSerializerRead
    post_serializer = TransactionSerializerPost

    @action(methods=['POST'], detail=False)
    def transact(self, request: Request):
        post_sr = self.post_serializer(data=request.data)

        post_sr.is_valid(raise_exception=True)

        transactions = self.service().transact(
            sender_id=post_sr.validated_data.get('sender_id'),
            inn_list=post_sr.validated_data.get('inn_to'),
            amount=post_sr.validated_data.get('amount')
        )
        read_sr = self.read_serializer(transactions, many=True)

        return Response(
            data=read_sr.data,
        )
