from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.forms import HiddenInput
from .models import Appointment
from .forms import AppointmentForm, AppointmentUpdateForm, AppointmentStatusForm
from .utils import can_modify_appointment
from mascotas.models import Mascota

def is_client_or_admin(user):
    return user.is_authenticated and (
        not (user.is_veterinario or user.is_secretaria) or 
        user.is_superuser
    )

@login_required
@user_passes_test(is_client_or_admin)
def crear_cita(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            
            # Si es un cliente, solo puede crear citas para sus propias mascotas
            if not request.user.is_superuser and not request.user.is_secretaria:
                if cita.mascota.propietario != request.user:
                    messages.error(request, 'Solo puedes crear citas para tus propias mascotas.')
                    return redirect('appointments:lista_citas')
                cita.cliente = request.user
            
            # Si es un admin o secretaria, puede crear citas para cualquier mascota
            else:
                # Asegurarse de que el cliente seleccionado sea el propietario de la mascota
                if cita.mascota.propietario != cita.cliente:
                    messages.error(request, 'El cliente seleccionado no es el propietario de la mascota.')
                    return render(request, 'appointments/formulario_cita.html', {'form': form})
            
            cita.save()
            messages.success(request, 'Cita creada con éxito.')
            return redirect('appointments:lista_citas')
    else:
        initial_data = {}
        if not request.user.is_superuser and not request.user.is_secretaria:
            initial_data['cliente'] = request.user
        
        form = AppointmentForm(initial=initial_data)
        
        if not request.user.is_superuser and not request.user.is_secretaria:
            form.fields['mascota'].queryset = Mascota.objects.filter(propietario=request.user)
            form.fields['cliente'].widget = HiddenInput()
            form.fields['cliente'].initial = request.user
    
    return render(request, 'appointments/formulario_cita.html', {'form': form})

@login_required
def lista_citas(request):
    if request.user.is_superuser:
        citas = Appointment.objects.all()
    elif request.user.is_veterinario:
        citas = Appointment.objects.filter(veterinario=request.user)
    else:
        citas = Appointment.objects.filter(cliente=request.user)

    # Aplicar filtros
    estado = request.GET.get('estado')
    veterinario = request.GET.get('veterinario')
    cliente = request.GET.get('cliente')
    
    if estado:
        citas = citas.filter(estado=estado)
    if veterinario and request.user.is_superuser:
        citas = citas.filter(veterinario__id=veterinario)
    if cliente and request.user.is_superuser:
        citas = citas.filter(cliente__id=cliente)
    
    paginator = Paginator(citas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'appointments/lista_citas.html', {'page_obj': page_obj})

@login_required
def detalle_cita(request, cita_id):
    cita = get_object_or_404(Appointment, id=cita_id)
    if not request.user.is_superuser and request.user != cita.cliente and request.user != cita.veterinario:
        messages.error(request, 'No tienes permiso para ver esta cita.')
        return redirect('appointments:lista_citas')
    return render(request, 'appointments/detalle_cita.html', {'cita': cita})

@login_required
def editar_cita(request, cita_id):
    cita = get_object_or_404(Appointment, id=cita_id)
    
    if not (request.user == cita.cliente or request.user.is_superuser or request.user.is_secretaria):
        messages.error(request, 'No tienes permiso para editar esta cita.')
        return redirect('appointments:lista_citas')
    
    if not can_modify_appointment(cita):
        messages.error(request, 'No se puede modificar la cita menos de 2 horas antes de la hora programada.')
        return redirect('appointments:detalle_cita', cita_id=cita.id)
    
    if request.method == 'POST':
        form = AppointmentUpdateForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada con éxito.')
            return redirect('appointments:detalle_cita', cita_id=cita.id)
    else:
        form = AppointmentUpdateForm(instance=cita)
    
    return render(request, 'appointments/formulario_cita.html', {'form': form, 'cita': cita})

@login_required
def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Appointment, id=cita_id)
    
    if not (request.user == cita.cliente or request.user.is_superuser or request.user.is_secretaria):
        messages.error(request, 'No tienes permiso para cancelar esta cita.')
        return redirect('appointments:lista_citas')
    
    if not can_modify_appointment(cita):
        messages.error(request, 'No se puede cancelar la cita menos de 2 horas antes de la hora programada.')
        return redirect('appointments:detalle_cita', cita_id=cita.id)
    
    if request.method == 'POST':
        cita.estado = 'CANCELADA'
        cita.save()
        messages.success(request, 'Cita cancelada con éxito.')
        return redirect('appointments:lista_citas')
    
    return render(request, 'appointments/confirmar_cancelar.html', {'cita': cita})

@login_required
@user_passes_test(lambda u: u.is_veterinario or u.is_superuser)
def actualizar_estado_cita(request, cita_id):
    cita = get_object_or_404(Appointment, id=cita_id)
    if request.method == 'POST':
        form = AppointmentStatusForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estado de la cita actualizado con éxito.')
            return redirect('appointments:detalle_cita', cita_id=cita.id)
    else:
        form = AppointmentStatusForm(instance=cita)
    return render(request, 'appointments/actualizar_estado.html', {'form': form, 'cita': cita})