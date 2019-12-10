from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import User
from .models import  Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        
        fields = [
            'phone_num',
            'name',
            'address',
            'get_message',
        ]
        widgets = {
            'phone_num': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'get_message': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


class CustomerForm2(forms.Form):
    phone_num = forms.CharField(label='고객번호')
    name = forms.CharField(label='고객명', max_length=30)


class OrderForm(forms.Form):
    est_date = forms.DateField(label='예상완료날짜',
        widget=forms.DateInput(
            attrs={'type': 'date'}
        ))
    requirements = forms.CharField(label='세부요청사항')


class SearchForm(forms.Form):
    word = forms.CharField(label='Search Word')


class SendMessageForm(forms.Form):
    customer_name = forms.CharField(label='이름', required=True)
    customer_number = forms.DecimalField(label='핸드폰 번호', required=True)

   # Options = (
   #     ('1', 'Hello'),
   #     ('2', 'World'),
   # )
   # category = forms.ChoiceField(label='Category', choices=Options)

    input_message = forms.CharField(label='문자 내용', required=True)
