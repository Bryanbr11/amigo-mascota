from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Sum, Case, When, Value, CharField, Avg, Count
from django.utils import timezone
from django.contrib.auth import get_user_model
from mascotas.models import Mascota
from consulta.models import Consulta
from appointments.models import Appointment
from notifications.models import Recordatorio
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from django.core.paginator import Paginator
from activity_logs.models import ActivityLog
from activity_logs.services import log_activity
from datetime import datetime, timedelta

User = get_user_model()

def is_admin(user):
    return user.is_superuser

def is_veterinario(user):
    return user.is_veterinario

def is_secretaria(user):
    return user.is_secretaria

def is_cliente(user):
    return not (user.is_superuser or user.is_veterinario or user.is_secretaria)

def home_view(request):
    # Redirige al dashboard si el usuario está autenticado
    if request.user.is_authenticated:
        return redirect('dashboard')
    # Si no está autenticado, muestra una página de bienvenida
    return render(request, 'home.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    # Registrar la actividad de acceso al dashboard
    log_activity(
        user=request.user,
        action_type='LOGIN',
        details='Acceso al panel de administración',
        request=request
    )
    
    hoy = timezone.now().date()
    mes_actual = timezone.now().month
    año_actual = timezone.now().year

    # Estadísticas de usuarios
    total_users = User.objects.count()
    veterinarios = User.objects.filter(is_veterinario=True).count()
    secretarias = User.objects.filter(is_secretaria=True).count()
    clientes = User.objects.filter(
        is_veterinario=False,
        is_secretaria=False,
        is_superuser=False
    ).count()
    clientes_activos = User.objects.filter(
        is_veterinario=False,
        is_secretaria=False,
        is_superuser=False,
        is_active=True
    ).count()

    # Estadísticas de mascotas
    total_mascotas = Mascota.objects.count()
    mascotas_nuevas = Mascota.objects.filter(
        fecha_registro__month=mes_actual,
        fecha_registro__year=año_actual
    ).count()

    # Estadísticas de citas
    total_citas = Appointment.objects.count()
    citas_pendientes = Appointment.objects.filter(estado='PENDIENTE').count()
    citas_hoy = Appointment.objects.filter(fecha=hoy).count()

    # Estadísticas de consultas e ingresos
    consultas_mes = Consulta.objects.filter(
        fecha__month=mes_actual,
        fecha__year=año_actual
    )
    total_consultas_mes = consultas_mes.count()
    ingresos_mes = consultas_mes.aggregate(
        total=Sum('costo')
    )['total'] or 0

    # Datos para el gráfico de citas por día
    ultimos_7_dias = [(timezone.now().date() - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    citas_por_dia = []
    for dia in ultimos_7_dias:
        citas_por_dia.append({
            'fecha': dia.strftime('%d/%m'),
            'total': Appointment.objects.filter(fecha=dia).count()
        })

    # Datos para el gráfico de ingresos por servicio
    ingresos_por_servicio = Consulta.objects.filter(
        fecha__month=mes_actual,
        fecha__year=año_actual
    ).values('tipo_servicio').annotate(
        total=Sum('costo')
    ).order_by('-total')

    # Obtener lista de empleados
    empleados = User.objects.filter(
        Q(is_veterinario=True) | 
        Q(is_secretaria=True) |
        Q(is_superuser=True)
    ).annotate(
        cargo=Case(
            When(is_superuser=True, then=Value('Administrador')),
            When(is_veterinario=True, then=Value('Veterinario')),
            When(is_secretaria=True, then=Value('Secretaria')),
            default=Value('Cliente'),
            output_field=CharField(),
        )
    ).order_by('-last_login')

    context = {
        'total_clientes': clientes,
        'clientes_activos': clientes_activos,
        'total_mascotas': total_mascotas,
        'mascotas_nuevas': mascotas_nuevas,
        'citas_pendientes': citas_pendientes,
        'citas_hoy': citas_hoy,
        'ingresos_mes': ingresos_mes,
        'total_consultas_mes': total_consultas_mes,
        'veterinarios': veterinarios,
        'secretarias': secretarias,
        'total_citas': total_citas,
        'total_consultas': Consulta.objects.count(),
        'citas_por_dia': citas_por_dia,
        'ingresos_por_servicio': ingresos_por_servicio,
        'empleados': empleados,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
@user_passes_test(is_veterinario)
def veterinario_dashboard(request):
    hoy = timezone.now().date()
    context = {
        'citas_hoy_count': Appointment.objects.filter(
            veterinario=request.user,
            fecha=hoy
        ).count(),
        'citas_pendientes': Appointment.objects.filter(
            veterinario=request.user,
            fecha=hoy,
            estado='PENDIENTE'
        ).count(),
        'pacientes_espera': Appointment.objects.filter(
            veterinario=request.user,
            fecha=hoy,
            estado='EN_ESPERA'
        ).count(),
        'consultas_mes': Consulta.objects.filter(
            veterinario=request.user,
            fecha__month=timezone.now().month
        ).count(),
        'proxima_cita': Appointment.objects.filter(
            veterinario=request.user,
            fecha=hoy,
            estado='PENDIENTE'
        ).order_by('hora').first(),
        'citas_hoy': Appointment.objects.filter(
            veterinario=request.user,
            fecha=hoy
        ).order_by('hora'),
        'pacientes_en_espera': Appointment.objects.filter(
            veterinario=request.user,
            fecha=hoy,
            estado='EN_ESPERA'
        ).order_by('hora'),
        'consultas_recientes': Consulta.objects.filter(
            veterinario=request.user
        ).order_by('-fecha')[:10]
    }
    return render(request, 'dashboard/veterinario_dashboard.html', context)

@login_required
@user_passes_test(is_secretaria)
def secretaria_dashboard(request):
    hoy = timezone.now().date()
    context = {
        'citas_hoy_count': Appointment.objects.filter(fecha=hoy).count(),
        'citas_pendientes_hoy': Appointment.objects.filter(
            fecha=hoy,
            estado='PENDIENTE'
        ).count(),
        'veterinarios_disponibles': User.objects.filter(
            is_veterinario=True,
            is_active=True
        ).count(),
        'pacientes_espera': Appointment.objects.filter(
            fecha=hoy,
            estado='EN_ESPERA'
        ).count(),
        'proxima_cita': Appointment.objects.filter(
            fecha=hoy,
            estado='PENDIENTE'
        ).order_by('hora').first(),
        'citas_hoy': Appointment.objects.filter(fecha=hoy).order_by('hora'),
        'recordatorios': Recordatorio.objects.filter(
            fecha=hoy,
            completado=False,
            creado_por=request.user
        ).order_by('hora')
    }
    return render(request, 'dashboard/secretaria_dashboard.html', context)

@login_required
@user_passes_test(is_cliente)
def cliente_dashboard(request):
    # Verificar si el usuario está autenticado y es cliente
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    if not is_cliente(request.user):
        if request.user.is_superuser:
            return redirect('dashboard:admin')
        elif request.user.is_veterinario:
            return redirect('dashboard:veterinario')
        elif request.user.is_secretaria:
            return redirect('dashboard:secretaria')
    
    context = {
        'mascotas_count': Mascota.objects.filter(propietario=request.user).count(),
        'proximas_citas_count': Appointment.objects.filter(
            cliente=request.user,
            fecha__gte=timezone.now().date(),
            estado='PENDIENTE'
        ).count(),
        'consultas_count': Consulta.objects.filter(
            mascota__propietario=request.user
        ).count(),
        'proximas_citas': Appointment.objects.filter(
            cliente=request.user,
            fecha__gte=timezone.now().date()
        ).order_by('fecha', 'hora')[:5]
    }
    return render(request, 'dashboard/cliente_dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def crear_usuario(request):
    # Verificación adicional de seguridad
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción')
        return redirect('dashboard:admin')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
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
                elif role == 'admin':
                    if not request.user.is_superuser:
                        messages.error(request, 'No tienes permisos para crear administradores')
                        return redirect('dashboard:admin')
                    user.is_superuser = True
                    user.is_staff = True
                
                # Registrar la actividad
                log_activity(
                    user=request.user,
                    action_type='CREATE',
                    details=f'Creación de usuario {user.username} con rol {role}',
                    request=request
                )
                
                user.save()
                messages.success(request, f'Usuario {user.username} creado exitosamente como {role}')
                return redirect('dashboard:gestionar_permisos')
                
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'dashboard/admin/crear_usuario.html', {
        'form': form,
        'is_admin': True
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def gestionar_permisos(request):
    # Obtener parámetros de filtrado
    role = request.GET.get('role', '')
    status = request.GET.get('status', '')
    search = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    # Iniciar el queryset
    users = User.objects.all()

    # Aplicar filtros
    if role:
        if role == 'veterinario':
            users = users.filter(is_veterinario=True)
        elif role == 'secretaria':
            users = users.filter(is_secretaria=True)
        elif role == 'admin':
            users = users.filter(is_superuser=True)
        elif role == 'cliente':
            users = users.filter(is_veterinario=False, is_secretaria=False, is_superuser=False)

    if status:
        users = users.filter(is_active=status == 'active')

    if search:
        users = users.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(username__icontains=search)
        )

    # Ordenar usuarios
    users = users.order_by('username')

    # Paginación
    paginator = Paginator(users, 10)  # 10 usuarios por página
    users_page = paginator.get_page(page)

    context = {
        'users': users_page,
        'current_role': role,
        'current_status': status,
        'search_query': search,
    }
    
    return render(request, 'dashboard/admin/gestionar_permisos.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def registros_actividad(request):
    # Obtener parámetros de filtrado
    user_id = request.GET.get('user', '')
    action_type = request.GET.get('action', '')
    date = request.GET.get('date', '')
    page = request.GET.get('page', 1)

    # Iniciar queryset
    logs = ActivityLog.objects.all()

    # Aplicar filtros
    if user_id:
        logs = logs.filter(user_id=user_id)
    if action_type:
        logs = logs.filter(action_type=action_type)
    if date:
        logs = logs.filter(timestamp__date=date)

    # Obtener usuarios para el filtro
    users = User.objects.filter(
        Q(is_superuser=True) |
        Q(is_veterinario=True) |
        Q(is_secretaria=True)
    ).order_by('username')

    # Paginación
    paginator = Paginator(logs, 20)  # 20 registros por página
    logs_page = paginator.get_page(page)

    context = {
        'users': users,
        'selected_user': user_id,
        'logs': logs_page,
        'current_action': action_type,
        'current_date': date,
    }
    
    return render(request, 'dashboard/admin/registros_actividad.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def reporte_ingresos(request):
    from consulta.models import Consulta
    from django.db.models import Sum, Avg
    from django.utils import timezone
    import datetime

    # Obtener parámetros de filtro
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    tipo_servicio = request.GET.get('tipo_servicio')

    # Si no hay fechas, usar el mes actual
    if not fecha_inicio:
        fecha_inicio = timezone.now().replace(day=1).date()
    else:
        fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()

    if not fecha_fin:
        fecha_fin = (fecha_inicio.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
    else:
        fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').date()

    # Construir el queryset base
    consultas = Consulta.objects.filter(fecha__date__range=[fecha_inicio, fecha_fin])

    if tipo_servicio:
        consultas = consultas.filter(tipo_servicio=tipo_servicio)

    # Calcular estadísticas
    total_ingresos = consultas.aggregate(total=Sum('costo'))['total'] or 0
    total_consultas = consultas.count()
    promedio_consulta = consultas.aggregate(promedio=Avg('costo'))['promedio'] or 0

    context = {
        'consultas': consultas.select_related('mascota', 'veterinario').order_by('-fecha'),
        'total_ingresos': total_ingresos,
        'total_consultas': total_consultas,
        'promedio_consulta': promedio_consulta,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'tipo_servicio': tipo_servicio,
        'tipos_servicio': Consulta.TIPO_SERVICIO_CHOICES,
    }

    return render(request, 'dashboard/admin/reporte_ingresos.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def estadisticas_servicios(request):
    return render(request, 'dashboard/admin/estadisticas_servicios.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def satisfaccion_clientes(request):
    # Obtener el rango de fechas (último mes por defecto)
    fecha_fin = timezone.now().date()
    fecha_inicio = fecha_fin - timedelta(days=30)

    # Calcular el promedio general de satisfacción
    promedio_general = Consulta.objects.filter(
        fecha__range=[fecha_inicio, fecha_fin],
        calificacion__isnull=False
    ).aggregate(
        promedio=Avg('calificacion')
    )['promedio'] or 0

    # Obtener el total de evaluaciones
    total_evaluaciones = Consulta.objects.filter(
        fecha__range=[fecha_inicio, fecha_fin],
        calificacion__isnull=False
    ).count()

    # Calcular el índice de recomendación (calificaciones >= 4)
    recomendaciones = Consulta.objects.filter(
        fecha__range=[fecha_inicio, fecha_fin],
        calificacion__gte=4
    ).count()
    indice_recomendacion = (recomendaciones / total_evaluaciones * 100) if total_evaluaciones > 0 else 0

    # Obtener desglose por categorías
    categorias = [
        {
            'nombre': 'Atención Veterinaria',
            'promedio': Consulta.objects.filter(
                fecha__range=[fecha_inicio, fecha_fin],
                tipo_servicio='CONSULTA_GENERAL'
            ).aggregate(avg=Avg('calificacion'))['avg'] or 0,
            'porcentaje': 85  # Ejemplo, ajustar según cálculo real
        },
        {
            'nombre': 'Tiempo de Espera',
            'promedio': 4.2,  # Ejemplo, ajustar según cálculo real
            'porcentaje': 75
        },
        {
            'nombre': 'Instalaciones',
            'promedio': 4.5,  # Ejemplo, ajustar según cálculo real
            'porcentaje': 90
        }
    ]

    # Obtener comentarios recientes
    comentarios_recientes = []
    consultas_recientes = Consulta.objects.filter(
        fecha__range=[fecha_inicio, fecha_fin],
        comentario__isnull=False
    ).exclude(
        comentario=''
    ).order_by('-fecha')[:5]

    for consulta in consultas_recientes:
        propietario = consulta.mascota.propietario
        nombre_cliente = propietario.get_full_name() if propietario.get_full_name() else propietario.username
        comentarios_recientes.append({
            'cliente': nombre_cliente,
            'fecha': consulta.fecha,
            'calificacion': consulta.calificacion,
            'texto': consulta.comentario
        })

    context = {
        'promedio_general': promedio_general,
        'total_evaluaciones': total_evaluaciones,
        'indice_recomendacion': round(indice_recomendacion),
        'categorias': categorias,
        'comentarios_recientes': comentarios_recientes,
    }

    return render(request, 'dashboard/admin/satisfaccion_clientes.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def configuracion_general(request):
    return render(request, 'dashboard/admin/configuracion_general.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def gestionar_servicios(request):
    return render(request, 'dashboard/admin/gestionar_servicios.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def respaldo_datos(request):
    return render(request, 'dashboard/admin/respaldo_datos.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_usuario(request, user_id):
    try:
        usuario = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('dashboard:gestionar_permisos')
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            role = request.POST.get('role')
            
            # Resetear todos los roles
            user.is_veterinario = False
            user.is_secretaria = False
            user.is_staff = False
            user.is_superuser = False
            
            # Asignar nuevo rol
            if role == 'veterinario':
                user.is_veterinario = True
                user.is_verified = True
            elif role == 'secretaria':
                user.is_secretaria = True
                user.is_staff = True
            elif role == 'admin':
                if not request.user.is_superuser:
                    messages.error(request, 'No tienes permisos para crear administradores')
                    return redirect('dashboard:gestionar_permisos')
                user.is_superuser = True
                user.is_staff = True
            
            user.save()
            messages.success(request, f'Usuario {user.username} actualizado exitosamente')
            return redirect('dashboard:gestionar_permisos')
    else:
        form = CustomUserChangeForm(instance=usuario)
        
    return render(request, 'dashboard/admin/editar_usuario.html', {
        'form': form,
        'usuario': usuario
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_estado_usuario(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción')
        return redirect('dashboard:gestionar_permisos')
        
    try:
        usuario = User.objects.get(id=user_id)
        
        # Evitar que un admin se desactive a sí mismo
        if usuario == request.user:
            messages.error(request, 'No puedes desactivar tu propio usuario')
            return redirect('dashboard:gestionar_permisos')
            
        # Evitar desactivar al último superusuario
        if usuario.is_superuser and User.objects.filter(is_superuser=True, is_active=True).count() <= 1:
            messages.error(request, 'No se puede desactivar al último administrador')
            return redirect('dashboard:gestionar_permisos')
        
        usuario.is_active = not usuario.is_active
        usuario.save()
        
        action = "activado" if usuario.is_active else "desactivado"
        messages.success(request, f'Usuario {usuario.username} {action} exitosamente')
        
    except User.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
    
    return redirect('dashboard:gestionar_permisos')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_usuarios(request):
    # Verificación adicional de seguridad
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción')
        return redirect('dashboard:admin')
    
    # Obtener todos los usuarios con sus roles anotados
    usuarios = User.objects.annotate(
        rol=Case(
            When(is_superuser=True, then=Value('Administrador')),
            When(is_veterinario=True, then=Value('Veterinario')),
            When(is_secretaria=True, then=Value('Secretaria')),
            default=Value('Cliente'),
            output_field=CharField(),
        )
    ).order_by('-date_joined')

    # Paginación
    paginator = Paginator(usuarios, 10)  # 10 usuarios por página
    page_number = request.GET.get('page')
    usuarios_page = paginator.get_page(page_number)

    context = {
        'usuarios': usuarios_page,
    }
    
    return render(request, 'dashboard/admin/listar_usuarios.html', context)
