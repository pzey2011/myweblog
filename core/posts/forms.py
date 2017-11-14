from django import forms


class CommentCreateForm(forms.Form):
    post_id=forms.IntegerField()
    text = forms.CharField(widget=forms.Textarea(attrs={'row': "2", 'class': 'materialize-textarea','placeholder':'Your Comment...'}))
    def clean(self):
        return self.cleaned_data