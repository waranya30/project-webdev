# ในไฟล์ menu/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Menu
from django.contrib.auth.forms import AuthenticationForm
from .models import TableReservation ,Table
from .models import Orders

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # เอา 'email' ออก
class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description','price', 'category','image','seller']
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="ชื่อผู้ใช้",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'ชื่อผู้ใช้'
        })
    )
    password = forms.CharField(
        label="รหัสผ่าน",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'รหัสผ่าน'
        })
    )

class OrderForm(forms.ModelForm):
    table = forms.ModelChoiceField(
        queryset=TableReservation.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Orders
        fields = ['menu', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'menu': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'menu': 'เลือกเมนู',
            'quantity': 'จำนวน',
            
        }

class TableReservationForm(forms.ModelForm):
    class Meta:
        model = TableReservation
        fields = ['table', 'customer_name', 'phone_number', 'reservation_date', 'reservation_time', 'number_of_people']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # แสดงเฉพาะโต๊ะที่ยังไม่ถูกจอง
        self.fields['table'].queryset = Table.objects.filter(is_reserved=False)