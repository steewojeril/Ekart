from django import forms
from owner.models import Products,Categories,Orders
class OrderUpdateForm(forms.Form):
    options=(
        ('dispatched','Dispatched'),
        ('in_transit','In Transit'),
        ('delivered','Delivered'),
    )
    status=forms.ChoiceField(choices=options,widget=forms.Select(attrs={'class':'form-select'}))
    expected_date=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Categories
        fields=['cat_name','is_active']
        widgets={
            'cat_name':forms.TextInput(attrs={'class':'form-control'}),
            'is_active':forms.CheckboxInput()
        }
class ProductForm(forms.ModelForm):
    class Meta:
        model=Products
        fields=['pro_name','description','price','image']
        widgets={
            'pro_name':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class': 'form-control','required':False}),
            
        }
