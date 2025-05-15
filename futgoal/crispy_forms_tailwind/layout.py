from crispy_forms.layout import (
    Layout as BaseLayout,
    Field as BaseField,
    Button as BaseButton,
    Submit as BaseSubmit,
    Hidden as BaseHidden,
    HTML as BaseHTML,
    Div as BaseDiv,
)

class Layout(BaseLayout):
    template_pack = 'tailwind'

class Field(BaseField):
    template = 'tailwind/field.html'

class Button(BaseButton):
    template = 'tailwind/layout/button.html'

class Submit(BaseSubmit):
    template = 'tailwind/layout/button.html'
    input_type = 'submit'

class Hidden(BaseHidden):
    template = 'tailwind/field.html'

class HTML(BaseHTML):
    template = 'tailwind/layout/html.html'

class Div(BaseDiv):
    template = 'tailwind/layout/div.html'
