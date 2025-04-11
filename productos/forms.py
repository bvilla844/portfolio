from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Product, CATEGORY_CHOICES, Customer, Order


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username...'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email...'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password...'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password...'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")
        return email


class ProductForm(forms.ModelForm):

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price',
                  'category', 'image', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio en pesos Colombianos'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['image'].required = False

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image and not self.instance.pk:
            raise forms.ValidationError("You must attach an image.")

        return image if image else self.instance.image

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return price


class ProductFilterForm(forms.Form):
    category_choices = Product._meta.get_field('category').choices
    category = forms.ChoiceField(
        choices=[('', 'Todas las categorías')] + list(category_choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class OrderForm(forms.ModelForm):
    phone = forms.CharField(max_length=10, required=True, label="Teléfono")
    address = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}), required=True, label="Dirección")
    payment_method = forms.ChoiceField(
        choices=Customer.payments,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Método de pago"
    )

    # Agregamos el campo 'status' con un desplegable
    status = forms.ChoiceField(
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Estado de la Orden"
    )

    class Meta:
        model = Order
        fields = ['payment_method', 'phone',
                  'address', 'status']  # Agregamos 'status'

    def __init__(self, *args, **kwargs):
        # Extraemos el usuario si se pasa como argumento
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Si el usuario no es staff, deshabilitar el campo 'status'
        if user and not user.is_staff:
            self.fields['status'].widget.attrs['disabled'] = 'disabled'
            # Forzar valor predeterminado
            self.fields['status'].initial = 'pendiente'


class OrderFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', '--- Filtrar por Estado ---'),
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'), 
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        required=False, 
        empty_label='--- Filtrar por Cliente ---'
    )
    date_created = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

