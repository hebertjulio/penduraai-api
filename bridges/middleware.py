from .models import Transaction


class LoadTransactionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        obj = None
        try:
            pk = self.get_PK(request.headers)
            if pk is not None:
                obj = Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            pass
        request.transaction = obj
        response = self.get_response(request)
        return response

    @classmethod
    def get_PK(cls, headers):
        if 'Transaction' not in headers:
            return None
        try:
            value = headers['Transaction']
            value = int(value)
            return value
        except ValueError:
            return None
