from django import forms
from django.forms.models import BaseInlineFormSet, BaseModelForm
from commonlab.models import ProjectPress, ProjectImpact

class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


class PersonQuestionForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea)
