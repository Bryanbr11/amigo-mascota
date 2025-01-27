from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import FichaMedica
from .forms import FichaMedicaForm
from django.contrib import messages

@login_required
@user_passes_test(lambda u: u.is_veterinario or u.is_superuser)
def crear_ficha_medica(request):
    if request.method == 'POST':
        form = FichaMedicaForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.veterinario = request.user
            ficha.save()
            messages.success(request, 'Ficha médica creada exitosamente')
            return redirect('medical_records:lista_fichas')
    else:
        form = FichaMedicaForm()
    return render(request, 'medical_records/crear_ficha.html', {'form': form})

@login_required
def lista_fichas_medicas(request):
    fichas = FichaMedica.objects.all()
    return render(request, 'medical_records/lista_fichas.html', {'fichas': fichas})

@login_required
def detalle_ficha_medica(request, ficha_id):
    ficha = get_object_or_404(FichaMedica, id=ficha_id)
    return render(request, 'medical_records/detalle_ficha.html', {'ficha': ficha})

# Create your views here.
