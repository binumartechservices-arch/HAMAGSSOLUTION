from django.contrib.auth.decorators import user_passes_test

def admin_required(view):
    return user_passes_test(lambda u: u.is_authenticated and u.is_admin)(view)

def salesman_required(view):
    return user_passes_test(lambda u: u.is_authenticated and u.is_salesman)(view)
