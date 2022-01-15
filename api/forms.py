from django import forms
from .models import Post, Lot, Wal

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','content',)

class Lotto(forms.ModelForm):

    class Meta:
        model = Lot
        fields = ('lot', 'id_code', 'description',)

class Wallet(forms.ModelForm):
    class Meta:
        model = Wal
        fields = ('ropsten','address','private_key', 'new_wallet',)