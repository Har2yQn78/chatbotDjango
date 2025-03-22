from django import forms

class QueryForm(forms.Form):
    query = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your query here...',
            'rows': 3,
        }),
        required=True,
        label='Query'
    )