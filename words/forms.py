from django import forms
from .models import Word

PARTS_OF_SPEECH = [
    ('noun', 'Noun'),
    ('verb', 'Verb'),
    ('adjective', 'Adjective'),
]

LEVELS = [
    ('a1', 'A1'),
    ('b1', 'B2'),
    ('c1', 'C3'),
]

class WordFilterForm(forms.Form):
    part_of_speech = forms.MultipleChoiceField(
        choices=PARTS_OF_SPEECH,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    level = forms.MultipleChoiceField(
        choices=LEVELS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
