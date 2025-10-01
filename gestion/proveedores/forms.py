from django import forms
from .models import OrdenCompra, DetalleOC

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['proveedor', 'fecha', 'total']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'total': forms.NumberInput(attrs={'step': '0.01'}),
        }

class DetalleOCForm(forms.ModelForm):
    class Meta:
        model = DetalleOC
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'precio_unitario': forms.NumberInput(attrs={'step': '0.01'}),
        }