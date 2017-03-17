from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Carroceiro

DAYS_WEEK = (
    (1, _('Domingo')),
    (2, _('Segunda-feira')),
    (3, _('Terça-feira')),
    (4, _('Quarta-feira')),
    (5, _('Quinta-feira')),
    (6, _('Sexta')),
    (7, _('Sábado')),
)


class DaysWeekWorkAdminForm(forms.ModelForm):
    days_week_work = forms.MultipleChoiceField(choices=DAYS_WEEK)

    class Meta:
        model = Carroceiro
        fields = '__all__'

    def clean_days_week_work(self):
        day = self.cleaned_data['days_week_work']
        if not day:
            raise forms.ValidationError("Informe um dia na semana")

        days = ','.join(day)
        return days
