from .forms import CalificacionForm
from django.shortcuts import render, redirect

def crear_calificacion(request):
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_calificacion')
    else:
        form = CalificacionForm()

    return render(request, 'calificaciones/crear.html', {'form': form})