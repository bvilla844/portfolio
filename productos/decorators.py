from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    """
    Restringe el acceso a usuarios autenticados. Si el usuario ya está logueado, lo redirige a 'home'.
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('products:home')
        return view_func(request, *args, **kwargs)
    
    return wrapper_func

def allowed_users(allowed_roles=[]):
    """
    Permite el acceso solo a usuarios con al menos uno de los roles permitidos.
    Si el usuario no tiene grupo o no pertenece a los roles permitidos, se le deniega el acceso.
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                user_roles = [group.name for group in request.user.groups.all()]  # Lista de grupos del usuario
                if any(role in allowed_roles for role in user_roles):  # Si al menos un rol coincide
                    return view_func(request, *args, **kwargs)
            return HttpResponse('You are not authorized to view this page', status=403)  # Respuesta 403 (Prohibido)
        return wrapper_func
    return decorator

def admin_only(view_func):
    """
    Restringe el acceso solo a usuarios en el grupo 'admin'.
    Si el usuario pertenece a 'customer', lo redirige a 'products'.
    """
    def wrapper_function(request, *args, **kwargs):
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            if group == 'customer':
                return redirect('products:products')  # Redirige a la lista de productos
            elif group == 'admin':
                return view_func(request, *args, **kwargs)
        return HttpResponse('You are not authorized to view this page', status=403)  # Bloquea a usuarios sin grupo
    
    return wrapper_function