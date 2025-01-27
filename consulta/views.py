from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseForbidden
from .models import Consulta, HistorialConsulta
from .forms import ConsultaForm, FinalizarConsultaForm
from mascotas.views import is_client_or_vet
from mascotas.models import Mascota
from django.utils import timezone
from .ia_diagnostico import generar_diagnostico_ia
from appointments.models import Appointment



def is_veterinario(user):
    return user.is_authenticated and user.is_veterinario

@login_required
def lista_consultas(request):
    if request.user.is_veterinario:
        consultas = Consulta.objects.filter(veterinario=request.user)
    else:
        consultas = Consulta.objects.filter(mascota__propietario=request.user)
    
    query = request.GET.get('q')
    if query:
        consultas = consultas.filter(
            Q(mascota__nombre__icontains=query) |
            Q(motivo__icontains=query) |
            Q(diagnostico__icontains=query)
        )
    
    paginator = Paginator(consultas, 10)
    page = request.GET.get('page')
    try:
        consultas = paginator.page(page)
    except PageNotAnInteger:
        consultas = paginator.page(1)
    except EmptyPage:
        consultas = paginator.page(paginator.num_pages)
    
    return render(request, 'consulta/lista_consultas.html', {'consultas': consultas})

@login_required
@user_passes_test(is_veterinario)
def crear_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.veterinario = request.user
            consulta.fecha = timezone.now().date()

            # Generar diagnóstico complementario con IA
            datos_consulta = {
                'sintomas': consulta.sintomas,
                'diagnostico': consulta.diagnostico,
                'peso': consulta.mascota.peso,
                'edad': consulta.mascota.edad,
                'raza': consulta.mascota.raza,
            }

            consulta.diagnostico_ia = generar_diagnostico_ia(datos_consulta)

            consulta.save()
            messages.success(request, 'Consulta creada con éxito.')
            return redirect('consulta:detalle_consulta', consulta_id=consulta.id)
    else:
        form = ConsultaForm()
    return render(request, 'consulta/formulario_consulta.html', {'form': form})

@login_required
def detalle_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if not request.user.is_veterinario and consulta.mascota.propietario != request.user:
        messages.error(request, 'No tienes permiso para ver esta consulta.')
        return redirect('consulta:lista_consultas')
    historial = consulta.historial.all()
    return render(request, 'consulta/detalle_consulta.html', {'consulta': consulta, 'historial': historial})

@login_required
@user_passes_test(is_veterinario)
def editar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id, veterinario=request.user)
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            HistorialConsulta.objects.create(
                consulta=consulta,
                diagnostico_anterior=consulta.diagnostico,
                tratamiento_anterior=consulta.tratamiento,
                notas_adicionales_anteriores=consulta.notas_adicionales,
                estado_anterior=consulta.estado
            )
            form.save()
            messages.success(request, 'Consulta actualizada con éxito.')
            return redirect('consulta:detalle_consulta', consulta_id=consulta.id)
    else:
        form = ConsultaForm(instance=consulta)
    return render(request, 'consulta/formulario_consulta.html', {'form': form, 'consulta': consulta})

@login_required
@user_passes_test(is_veterinario)
def finalizar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id, veterinario=request.user)
    if request.method == 'POST':
        form = FinalizarConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            HistorialConsulta.objects.create(
                consulta=consulta,
                diagnostico_anterior=consulta.diagnostico,
                tratamiento_anterior=consulta.tratamiento,
                notas_adicionales_anteriores=consulta.notas_adicionales,
                estado_anterior=consulta.estado
            )    
            form.save()
            messages.success(request, 'Consulta finalizada con éxito.')
            return redirect('consulta:detalle_consulta', consulta_id=consulta.id)
    else:
        form = FinalizarConsultaForm(instance=consulta)    
    return render(request, 'consulta/formulario_consulta.html', {'form': form, 'consulta': consulta})


@login_required
def cancelar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    if request.method == 'POST':
        consulta.estado = 'CANCELADA'
        consulta.save()
        # Puedes añadir un mensaje de éxito aquí si lo deseas
        return redirect('consulta:lista_consultas')  # Asegúrate de que esta URL exista
    return render(request, 'consulta/confirmar_cancelacion.html', {'consulta': consulta})


@login_required
@user_passes_test(is_client_or_vet)
def consultas_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    consultas = Consulta.objects.filter(mascota=mascota)
    return render(request, 'consulta/consultas_mascota.html', {'mascota': mascota, 'consultas': consultas})

@login_required
def diagnostico_detalle(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id, propietario=request.user)
    return render(request, 'consulta/diagnostico_detalle.html', {'consulta': consulta})

@login_required
def historial_medico(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id, propietario=request.user)
    consultas = Consulta.objects.filter(mascota=mascota).order_by('-fecha')
    return render(request, 'consulta/historial_medico.html', {'mascota': mascota, 'consultas': consultas})

@login_required
def descargar_diagnostico_pdf(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id, mascota__dueno=request.user)
    
    # Crear un objeto BytesIO para guardar el PDF
    buffer = BytesIO()
    
    # Crear el objeto PDF usando ReportLab
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Añadir contenido al PDF
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, f"Diagnóstico de {consulta.mascota.nombre}")
    p.drawString(100, 730, f"Fecha: {consulta.fecha.strftime('%d/%m/%Y')}")
    p.drawString(100, 710, f"Propietario: {consulta.mascota.dueno.get_full_name()}")
    
    p.drawString(100, 680, "Síntomas:")
    textobject = p.beginText(120, 660)
    for line in consulta.sintomas.split('\n'):
        textobject.textLine(line)
    p.drawText(textobject)
    
    p.drawString(100, 620, "Diagnóstico:")
    textobject = p.beginText(120, 600)
    for line in consulta.diagnostico.split('\n'):
        textobject.textLine(line)
    p.drawText(textobject)
    
    p.drawString(100, 560, "Tratamiento:")
    textobject = p.beginText(120, 540)
    for line in consulta.tratamiento.split('\n'):
        textobject.textLine(line)
    p.drawText(textobject)
    
    # Cerrar el objeto PDF
    p.showPage()
    p.save()
    
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

@login_required
@user_passes_test(is_veterinario)
def historial_consultas(request):
    consultas = Consulta.objects.filter(veterinario=request.user).order_by('-fecha')
    return render(request, 'consulta/historial_consultas.html', {
        'consultas': consultas
    })

@login_required
@user_passes_test(is_veterinario)
def crear_consulta_desde_cita(request, cita_id):
    cita = get_object_or_404(Appointment, id=cita_id, veterinario=request.user)
    
    if request.method == 'POST':
        try:
            consulta = Consulta.objects.create(
                mascota=cita.mascota,
                veterinario=request.user,
                fecha=timezone.now(),
                motivo=cita.motivo,
                diagnostico=request.POST.get('diagnostico'),
                tratamiento=request.POST.get('tratamiento'),
                observaciones=request.POST.get('observaciones'),
                costo=request.POST.get('costo')
            )
            
            # Actualizar estado de la cita
            cita.estado = 'COMPLETADA'
            cita.save()
            
            messages.success(request, 'Consulta creada exitosamente')
            return redirect('consulta:detalle_consulta', consulta_id=consulta.id)
        except Exception as e:
            messages.error(request, f'Error al crear la consulta: {str(e)}')
    
    return render(request, 'consulta/crear_consulta.html', {
        'cita': cita
    })