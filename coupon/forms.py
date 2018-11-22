from django.contrib.auth.forms import UserCreationForm

from django import forms
from . import models
class CouponForm(forms.ModelForm):

    class Meta():
        model= models.Coupon
        
        fields=('cafe','discount','start_date','end_date','mob_number')
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cafe'].queryset = models.Cafe.objects.all()


        # widgets= {
        #     'title':forms.TextInput(attrs={'class':'textinputclass'}),
        #     'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        # }


class ValidatorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_validator = True
        if commit:
            user.save()
        return user


class GeneratorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_generator = True
        if commit:
            user.save()
        return user

class ValidateForm(forms.ModelForm):
    
    
    class Meta:
        model=models.Coupon
        fields = ('coupon_id',)
    
    