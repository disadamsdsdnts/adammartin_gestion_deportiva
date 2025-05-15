from django import template
from crispy_forms.templatetags.crispy_forms_field import CrispyFieldNode

register = template.Library()

@register.tag(name="crispy_field")
def crispy_field(parser, token):
    """
    Template tag that renders a field using the tailwind template pack
    """
    return CrispyFieldNode(token.split_contents()[1], 'tailwind')
