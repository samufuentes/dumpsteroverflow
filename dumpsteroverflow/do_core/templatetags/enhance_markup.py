from django import template
register = template.Library()

@register.filter(name='add_attrs')
def add_attrs(field, attrs_str):
  attrs = {}
  attr_name_values = attrs_str.split(',')

  for a in attr_name_values:
      t, v = a.split(':')
      attrs[t] = v

  return field.as_widget(attrs=attrs)
