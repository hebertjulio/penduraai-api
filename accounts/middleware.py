from .models import Profile


class LoadProfileMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        profile = self.get_object(request)
        if profile:
            request.profile = profile
        response = self.get_response(request)
        return response

    @classmethod
    def get_object(cls, request):
        pk = cls.get_pk(request.headers)
        if not pk:
            return None
        try:
            obj = Profile.objects.get(pk=pk)
            return obj
        except Profile.DoesNotExist:
            pass
        return None

    @classmethod
    def get_pk(cls, headers):
        try:
            value = headers['Profile']
            value = int(value)
            return value
        except (KeyError, ValueError):
            return None
