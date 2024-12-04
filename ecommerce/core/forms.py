from django import forms
from .models import ProductReview


class reviewForm(forms.ModelForm):

    review = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "write review",
                "id": "review-text",
                "name": "review",
                "class": "form-control",
                "rows": "4",
            }
        )
    )

    class Meta:
        model = ProductReview
        fields = ["review", "rating"]
