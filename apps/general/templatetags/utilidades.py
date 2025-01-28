from django import template

register =  template.Library()

@register.filter(name='montoFormateado')
def montoFormateado(monto):
    if monto != 0:
        monto = "{:,}".format(monto).replace(",", ".")
    else:
      monto = "0"
    return monto


@register.filter
def filter_by(queryset, arg):
    """
    Filtra un queryset dinámicamente usando una cadena de tipo 'key:value'.
    """
    if not arg or ':' not in arg:
        # Retornar queryset sin filtrar si el argumento no es válido
        return queryset
    try:
        key, value = arg.split(':', 1)
        return queryset.filter(**{key: value})
    except ValueError:
        raise ValueError(f"El argumento '{arg}' no está en el formato 'key:value'")

@register.filter(name='montoConPuntos')
def montoConPuntos(monto):
    try:
        # Asegúrate de que el monto es un número
        monto = int(monto)
        # Formatea el número con puntos como separadores de miles
        return f"{monto:,}".replace(",", ".")
    except (ValueError, TypeError):
        # Si el monto no es un número válido, devuélvelo como está
        return monto

@register.filter(name='textoConEspacios')
def textoConEspacios(texto):
    return texto.replace("_", " ")