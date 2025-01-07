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
