from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import  get_object_or_404, render, redirect

from .forms import LoginForm, RegisterForm, CooperationForm, PurchaseForm
from .models import Product, Korzina, ProductKorzina


def main(request):
    """Главная страница."""

    template = 'pages/about.html'
    return render(request, template)


def catalog(request):
    """Отображение каталога продуктов."""

    template = 'pages/catalog.html'
    products = Product.objects.all()
    return render(request, template, {'catalog': products, 'purchase_form': PurchaseForm()})


def purchase_product(request, product_id):
    """Обработка покупки товара."""

    template = 'pages/korzina.html'
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PurchaseForm(request.POST)
            if form.is_valid():
                try:
                    volume = form.cleaned_data['volume']
                    quantity = form.cleaned_data['quantity']
                    phone = form.cleaned_data['phone']
                    email = form.cleaned_data['email']
                    korzina, created = Korzina.objects.get_or_create(user=user)
                    product_korzina, created = ProductKorzina.objects.get_or_create(
                        product=product,
                        korzina=korzina,
                        email=email,
                        phone=phone,
                        defaults={'volume': volume, 'quantity': quantity}
                    )
                    if not created:
                        product_korzina.quantity += quantity
                        product_korzina.save()
                    messages.success(request, 'Продукт успешно добавлен в корзину!')
                    return redirect('pages:catalog')
                except Exception as e:
                    messages.error(request, e)
                    return redirect('pages:catalog')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
                return redirect('pages:catalog')
        else:
            messages.error(request, 'Вы не зарегестрированы!')
            return redirect('pages:catalog')
    else:
        form = PurchaseForm()
    return render(request, template, {'purchase_form': form, 'product': product})


def korzina(request):
    """Корзина."""

    template = 'pages/korzina.html'
    if request.user.is_authenticated:
        korzina = Korzina.objects.filter(user=request.user).first()
        if korzina:
            products_in_korzina = ProductKorzina.objects.filter(korzina=korzina).select_related('product')
            return render(request, template, {'products_in_korzina': products_in_korzina})
    return render(request, template, {'products_in_korzina': []})

def cooperation(request):
    """Сотрудничество."""

    template = 'pages/communicate.html'
    form_cooperation = CooperationForm()
    if request.method == 'POST':
        form_cooperation = CooperationForm(request.POST)
        if form_cooperation.is_valid():
            form_cooperation.save()
            messages.success(request, 'Вы успешно отправили заявку!')
            return redirect('pages:cooperation')
        else:
            for field, errors in form_cooperation.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
            return redirect('pages:cooperation')
    return render(request, template, {'cooperation_form': form_cooperation})


def login_view(request):
    """Обработка запроса на вход юзера."""

    template = 'pages/about.html'
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно залогинились!')
            return redirect('pages:about')
        else:
            messages.error(request, 'Неверный логин или пароль')
            return redirect('pages:about')

    return render(request, template, {'login_form': form})


def register_view(request):
    """Обработка запроса на регистрацию юзера."""

    template = 'pages/about.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('pages:about')
        else:
            errors_dict = {}
            for field, errors in form.errors.items():
                errors_dict[field] = errors
            return render(request, template, {'register_form': form, 'errors': errors_dict})
    else:
        form = RegisterForm()

    return render(request, template, {'register_form': form})


def logout_view(request):
    """Для разлогина юзера."""

    logout(request)
    return redirect('pages:about')
