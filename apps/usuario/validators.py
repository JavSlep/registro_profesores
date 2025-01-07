from django.core.exceptions import ValidationError

def validation_password(value):
    errors = []
    if len(value) < 8:
        errors.append(ValidationError('La contraseña debe tener al menos 8 caracteres.'))
    if len(value) > 15:
        errors.append(ValidationError('La contraseña debe tener un máximo de 15 caracteres.'))
    if not any(char.isdigit() for char in value):
        errors.append(ValidationError('La contraseña debe contener al menos un número.'))
    if not any(char.isupper() for char in value):
        errors.append(ValidationError('La contraseña debe contener al menos una letra mayúscula.'))
    if not any(char.islower() for char in value):
        errors.append(ValidationError('La contraseña debe contener al menos una letra minúscula.'))
    if errors:
        raise ValidationError(errors)