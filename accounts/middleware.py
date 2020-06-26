from .models import Profile


class LoadProfileMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        obj = None
        try:
            pk = self.get_PK(request.headers)
            if pk is not None:
                obj = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            pass
        request.profile = obj
        response = self.get_response(request)
        return response

    @classmethod
    def get_PK(cls, headers):
        if 'Profile' not in headers:
            return None
        name, value = headers['Profile'].split()
        if name.upper() != 'PK':
            return None
        try:
            value = int(value)
            return value
        except ValueError:
            return None
