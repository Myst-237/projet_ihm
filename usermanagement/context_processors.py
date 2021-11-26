from .models import CustomUser

def get_roles(request):
    if request.user.is_authenticated:
        return {'roles': request.user.role}
    else:
        return {'roles': []}