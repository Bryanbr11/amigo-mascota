from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user

def jwt_auth_middleware(get_response):
    def middleware(request):
        request.user = SimpleLazyObject(lambda: get_user_jwt(request))
        return get_response(request)
    return middleware

def get_user_jwt(request):
    user = get_user(request)
    if user.is_authenticated:
        return user
    jwt_authentication = JWTAuthentication()
    try:
        user_auth_tuple = jwt_authentication.authenticate(request)
    except:
        return None
    if user_auth_tuple is not None:
        request.user, _ = user_auth_tuple
    return request.user

class CSRFDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            csrf_token = request.META.get('CSRF_COOKIE', None)
            post_token = request.POST.get('csrfmiddlewaretoken', None)
            print(f"CSRF Cookie Token: {csrf_token}")
            print(f"POST Token: {post_token}")
        
        response = self.get_response(request)
        return response