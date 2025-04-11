from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .forms import CreateUserForm, ProductForm, OrderForm, ProductFilterForm, OrderFilterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Customer, Order
from .decorators import unauthenticated_user, admin_only
from datetime import datetime  # <--- Agregar esta línea
from django.utils import timezone



@login_required(login_url='signin')
def home(request):
    return render(request, 'productos/home.html')


@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Agregar el usuario al grupo "customer"
            customer_group, created = Group.objects.get_or_create(
                name='customer')
            user.groups.add(customer_group)

            # 🔹 Crear un perfil de cliente automáticamente
            Customer.objects.create(
                user=user,
                name=user.username,  # Puedes personalizar este valor
                email=user.email  # Puedes agregar más campos si es necesario
            )

            messages.success(
                request, f'{user.username}, cuenta creada exitosamente')
            return redirect('products:signin')

    context = {'form': form}
    return render(request, 'productos/register.html', context)


@unauthenticated_user
def signin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('products:home')
        else:
            messages.info(request, 'Usuario o constraseña son incorrectas')
    context = {}
    return render(request, 'productos/signin.html', context)
    

@login_required(login_url='products:signin')
def singout(request):
    logout(request)
    return redirect('products:signin')


@login_required(login_url='products:signin')
def products(request):
    # Usamos GET para que los filtros vengan en la URL
    form = ProductFilterForm(request.GET)
    products = Product.objects.all()  # Obtener todos los productos por defecto

    if form.is_valid():
        # Obtener la categoría seleccionada
        category = form.cleaned_data.get('category')
        if category:  # Si el usuario seleccionó una categoría, filtrar
            products = products.filter(category=category)

    context = {
        'products': products,
        'form': form,
    }
    return render(request, 'productos/products.html', context)


@login_required
@admin_only
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            messages.success(request, "Producto creado exitosamente.")
            return redirect('products:products')
        else:
            messages.error(request, "Hubo un error al crear el producto.")
    else:
        form = ProductForm()

    return render(request, 'productos/create_product.html', {'form': form})


@login_required
@admin_only
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            updated_product = form.save(commit=False)

            if not request.FILES.get('image'):
                updated_product.image = product.image

            updated_product.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('products:products')
        else:
            messages.error(request, "Hubo un error al actualizar el producto.")
    else:
        form = ProductForm(instance=product)

    return render(request, 'productos/product_detail.html', {'product': product, 'form': form})


@login_required
@admin_only
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Producto eliminado correctamente.")
        # Asegúrate de que 'products' sea la URL correcta para la lista de productos.
        return redirect('products:products')

    messages.error(
        request, "Ocurrió un error al intentar eliminar el producto.")
    return redirect('products:product_detail', product_id=product.id)


@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'productos/buy_product.html', context)


@login_required
def order_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not product.is_available:
        messages.error(
            request, "El producto no está disponible para la compra.")
        return redirect('products:product_detail', product_id=product.id)

    customer = get_object_or_404(Customer, user=request.user)

    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.product = product

            # Si el usuario no es staff, forzar el estado "pendiente"
            if not request.user.is_staff:
                order.status = 'pendiente'

            order.save()
            messages.success(request, "Orden generada correctamente.")
            return redirect('products:products')
        else:
            print(form.errors)  # Depuración en consola

    else:
        form = OrderForm(
            initial={
                'payment_method': customer.payment,
                'phone': customer.phone,
                'address': customer.address,
                'status': 'pendiente'
            },
            user=request.user
        )

    context = {
        'form': form,
        'customer': customer,
        'user_name': customer.user.username,
        'user_email': customer.user.email,
        'product': product
    }
    return render(request, 'productos/order_product.html', context)


@login_required
@admin_only
def orders(request):
    form = OrderFilterForm(request.GET)
    orders = Order.objects.all()

    if form.is_valid():
        status = form.cleaned_data.get('status')
        customer = form.cleaned_data.get('customer')
        date_created = form.cleaned_data.get('date_created')

        if status:
            orders = orders.filter(status=status)
        if customer:
            orders = orders.filter(customer=customer)
        if date_created:
            # Convertir la fecha a timezone-aware
            date_created = timezone.make_aware(
                datetime.combine(date_created, datetime.min.time())
            )
            # Filtrar por fecha exacta
            orders = orders.filter(date_created__date=date_created.date())

    context = {
        'orders': orders,
        'form': form,
    }
    return render(request, 'productos/orders.html', context)


@login_required
@admin_only
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)  # Corregido

    if request.method == 'POST':
        # Asociar la instancia correcta
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Orden actualizada correctamente.")
            return redirect('products:orders')  # Redirigir a la lista de órdenes
        else:
            messages.error(request, "Hubo un error al actualizar la orden.")
    else:
        form = OrderForm(instance=order)

    return render(request, 'order_detail.html', {'order': order, 'form': form})


@login_required
@admin_only
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.delete()
        messages.success(request, "Orden eliminada correctamente.")
        return redirect('products:orders')

    messages.error(
        request, "Ocurrió un error al intentar eliminar el producto.")
    return redirect('products:product_detail', product_id=order.id)


@login_required
def sell(request):
    return render(request, 'productos/sell.html')


@login_required
def total_orders(request):
    user = request.user
    customer = user.customer
    orders = Order.objects.filter(customer=customer, status='pendiente')

    total_products = 0
    total_price = 0
    product_details = []

    for order in orders:
        total_products += 1
        total_price += order.product.price
        product_details.append(order.product)

    context = {
        'orders': orders,
        'total_products': total_products,
        'total_price': total_price,
        'product_details': product_details,  # Pasamos los detalles de los productos
    }

    return render(request, 'productos/total_orders.html', context)


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.customer.user == request.user:
        order.status = 'cancelado'
        order.save()
    return redirect('products:total_orders')
