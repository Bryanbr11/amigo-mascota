from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Mascota
from .forms import MascotaForm
from .filters import MascotaFilter

def is_client_or_vet(user):
    return user.is_authenticated and (
        not (user.is_veterinario or user.is_secretaria or user.is_superuser) or 
        user.is_veterinario
    )

def is_client(user):
    return user.is_authenticated and not (user.is_veterinario or user.is_secretaria or user.is_superuser)

@login_required
@user_passes_test(is_client_or_vet)
def lista_mascotas(request):
    # Verificar si el usuario es cliente (no es veterinario, secretaria ni superusuario)
    if not (request.user.is_veterinario or request.user.is_secretaria or request.user.is_superuser):
        mascotas_list = Mascota.objects.filter(propietario=request.user)
    else:  # Es veterinario
        mascotas_list = Mascota.objects.all()
    
    mascota_filter = MascotaFilter(request.GET, queryset=mascotas_list)
    mascotas_list = mascota_filter.qs
    
    paginator = Paginator(mascotas_list, 10)
    page = request.GET.get('page')
    try:
        mascotas = paginator.page(page)
    except PageNotAnInteger:
        mascotas = paginator.page(1)
    except EmptyPage:
        mascotas = paginator.page(paginator.num_pages)
    
    return render(request, 'mascotas/lista_mascotas.html', {
        'mascotas': mascotas,
        'filter': mascota_filter
    })

@login_required
@user_passes_test(is_client_or_vet)
def detalle_mascota(request, mascota_id):
    # Verificar si el usuario es cliente
    if not (request.user.is_veterinario or request.user.is_secretaria or request.user.is_superuser):
        mascota = get_object_or_404(
            Mascota.objects.select_related('propietario'),
            id=mascota_id,
            propietario=request.user
        )
    else:  # Es veterinario
        mascota = get_object_or_404(
            Mascota.objects.select_related('propietario'),
            id=mascota_id
        )
    return render(request, 'mascotas/detalle_mascota.html', {'mascota': mascota})

@login_required
@user_passes_test(is_client)
def crear_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.propietario = request.user
            mascota.save()
            messages.success(request, "Mascota registrada con éxito.")
            return redirect('mascotas:lista')
    else:
        form = MascotaForm()
    return render(request, 'mascotas/formulario_mascota.html', {'form': form})

@login_required
@user_passes_test(is_client)
def editar_mascota(request, mascota_id):
    try:
        mascota = Mascota.objects.get(id=mascota_id, propietario=request.user)
    except Mascota.DoesNotExist:
        messages.error(request, "La mascota no existe o no tienes permiso para editarla.")
        return redirect('mascotas:lista')

    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, "Mascota actualizada con éxito.")
            return redirect('mascotas:detalle', mascota_id=mascota.id)
    else:
        form = MascotaForm(instance=mascota)
    return render(request, 'mascotas/formulario_mascota.html', {'form': form, 'mascota': mascota})

@login_required
@user_passes_test(is_client)
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id, propietario=request.user)
    if request.method == 'POST':
        mascota.delete()
        messages.success(request, "Mascota eliminada correctamente.")
        return redirect('mascotas:lista')
    return render(request, 'mascotas/confirmar_eliminar.html', {'mascota': mascota})
