from .models import CustomUser

def get_roles(request):
    if request.user.is_authenticated:
        return {'roles': request.user.role}
    else:
        return {'roles': []}
    
def get_active_role(request):
    if request.user.is_authenticated:
        return {'active_role': request.user.active_role}
    else:
        return {'active_role':''}