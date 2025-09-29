from django import forms
from .models import OrdenCompra, DetalleOC

class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['proveedor', 'fecha', 'total']

class DetalleOCForm(forms.ModelForm):
    class Meta:
        model = DetalleOC
        fields = ['producto', 'cantidad', 'precio_unitario']