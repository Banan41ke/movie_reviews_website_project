# movies/forms.py
from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '★☆☆☆☆ - Ужасно'),
        (2, '★★☆☆☆ - Плохо'),
        (3, '★★★☆☆ - Средне'),
        (4, '★★★★☆ - Хорошо'),
        (5, '★★★★★ - Отлично'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,  # Теперь только 1-5
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        label='Ваша оценка'
    )

    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Напишите ваш отзыв...'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Оставьте комментарий...'
            }),
        }
        labels = {
            'text': 'Комментарий',
        }