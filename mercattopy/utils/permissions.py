def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def is_operador(user):
    return user.groups.filter(name="Operador").exists()