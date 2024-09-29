from django.shortcuts import render, redirect
from .models import Cliente, Cancha, Reserva, UserProfile
from .forms import ClienteForm, CanchaForm, ReservaForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    return render(request, 'reservas/index.html')

def cliente_list(request):
    query = Cliente.objects.all()
    context = {"object_list": query}
    return render(request, 'reservas/cliente_list.html', context)

def cancha_list(request):
    query = Cancha.objects.all()
    context = {"object_list": query}
    return render(request, 'reservas/cancha_list.html', context)

def reserva_list(request):
    query = Reserva.objects.all()
    context = {"object_list": query}
    return render(request, 'reservas/reserva_list.html', context)

def cliente_create(request):
    if request.method == 'GET':
        form = ClienteForm()
    elif request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    return render(request, 'reservas/cliente_create.html', {'form': form})

def cancha_create(request):  
    """
    View para crear una cancha. Utiliza el formulario CanchaForm.

    Si el request es GET, se crea un formulario vacio y se renderiza el
    template cancha_create.html con el formulario.

    Si el request es POST, se crea un formulario con los datos del
    request y se comprueba su validez. Si es válido, se guarda el formulario
    y se redirige a la lista de canchas. Si no es válido, se renderiza de
    nuevo el template con el formulario y los errores.
    """

    if request.method == 'GET':
        form = CanchaForm()
    elif request.method == 'POST':  # Cambiado a elif
        form = CanchaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cancha_list')
    return render(request, 'reservas/cancha_create.html', {'form': form})

def reserva_create(request):
    if request.method == 'GET':
        form = ReservaForm()
    elif request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reserva_list')
    return render(request, 'reservas/reserva_create.html', {'form': form})

def cliente_update(request, pk):
    cliente = Cliente.objects.get(pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'reservas/cliente_create.html', {'form': form})

def cliente_delete(request, pk):
    cliente = Cliente.objects.get(pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_list')
    return render(request, 'reservas/cliente_confirm_delete.html', {'object': cliente})

def cancha_update(request, pk):
    cancha = Cancha.objects.get(pk=pk)
    if request.method == 'POST':
        form = CanchaForm(request.POST, instance=cancha)
        if form.is_valid():
            form.save()
            return redirect('cancha_list')
    else:
        form = CanchaForm(instance=cancha)
    return render(request, 'reservas/cancha_create.html', {'form': form})

def cancha_delete(request, pk):
    cancha = Cancha.objects.get(pk=pk)
    if request.method == 'POST':
        cancha.delete()
        return redirect('cancha_list')
    return render(request, 'reservas/cancha_confirm_delete.html', {'object': cancha})

def reserva_update(request, pk):
    reserva = Reserva.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('reserva_list')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'reservas/reserva_create.html', {'form': form})

def reserva_delete(request, pk):
    reserva = Reserva.objects.get(pk=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('reserva_list')
    return render(request, 'reservas/reserva_confirm_delete.html', {'object': reserva})

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Cambia esto a la URL de tu elección
    else:
        form = CustomUserCreationForm()
    return render(request, 'reservas/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'reservas/login.html', {'form': form, 'error': 'Credenciales inválidas'})
    else:
        form = AuthenticationForm()
    return render(request, 'reservas/login.html', {'form': form})

@login_required
def profile(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirigir a la página de perfil
    else:
        form = CustomUserCreationForm(instance=request.user)
    return render(request, 'reservas/profile.html', {'form': form})

def custom_logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')  # Redirige a la página de inicio después de logout
    return redirect('index')  # Si intentan un método GET, también los redirige

def about(request):
    return render(request, 'reservas/about.html')

@login_required
def edit_profile(request):
    # Asegurarse de que el perfil del usuario existe, y si no, crearlo
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # Guarda el perfil con la foto actualizada
            return redirect('profile')  # Redirigir a la vista de perfil después de guardar
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'reservas/edit_profile.html', {'form': form})
