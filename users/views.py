from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.decorators.csrf import ensure_csrf_cookie

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            if user.is_superuser:
                return redirect('dashboard:admin_dashboard')
            elif user.is_veterinario:
                return redirect('dashboard:veterinario_dashboard')
            elif user.is_secretaria:
                return redirect('dashboard:secretaria_dashboard')
            else:
                return redirect('dashboard:cliente_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('users:perfil')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

@ensure_csrf_cookie
def custom_login(request):
    if request.user.is_authenticated:
        # Si ya está autenticado, redirigir según su rol
        if request.user.is_superuser:
            return redirect('dashboard:admin_dashboard')
        elif request.user.is_veterinario:
            return redirect('dashboard:veterinario_dashboard')
        elif request.user.is_secretaria:
            return redirect('dashboard:secretaria_dashboard')
        else:
            return redirect('dashboard:cliente_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Por favor ingrese usuario y contraseña')
            return render(request, 'users/login.html')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Registrar el login exitoso
                from activity_logs.services import log_activity
                log_activity(
                    user=user,
                    action_type='LOGIN',
                    details=f'Inicio de sesión exitoso - IP: {request.META.get("REMOTE_ADDR")}',
                    request=request
                )
                
                # Redirigir según el rol del usuario
                if user.is_superuser:
                    return redirect('dashboard:admin_dashboard')
                elif user.is_veterinario:
                    return redirect('dashboard:veterinario_dashboard')
                elif user.is_secretaria:
                    return redirect('dashboard:secretaria_dashboard')
                else:
                    return redirect('dashboard:cliente_dashboard')
            else:
                messages.error(request, 'Tu cuenta está desactivada')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'users/login.html')

def staff_home(request):
    return render(request, 'staff_home.html')

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='users:login')
def staff_register(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('users:login')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = request.POST.get('role')
            
            # Asignar rol según la selección
            if role == 'veterinario':
                user.is_veterinario = True
                user.is_verified = True
                user.license_number = form.cleaned_data.get('license_number', '')
            elif role == 'secretaria':
                user.is_secretaria = True
                user.is_staff = True
            
            try:
                user.save()
                messages.success(request, f'Usuario {user.username} creado exitosamente como {role}')
                return redirect('dashboard:admin_dashboard')
            except Exception as e:
                messages.error(request, str(e))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/staff_register.html', {
        'form': form
    })