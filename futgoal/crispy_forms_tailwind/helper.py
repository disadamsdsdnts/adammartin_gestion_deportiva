from crispy_forms.helper import FormHelper as BaseFormHelper

class FormHelper(BaseFormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_pack = 'tailwind'
        self.form_class = 'space-y-4 md:space-y-6'
