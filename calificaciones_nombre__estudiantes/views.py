from django.shortcuts import render

# Create your views here.
def crear_calificacion(request):
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar')
    else:
        form = CalificacionForm()

    return render(request, 'calificaciones/crear.html', {'form': form})

def listar_calificaciones(request):
    calificaciones = Calificacion.objects.all()
    return render(request, 'calificaciones/listar.html', {
        'calificaciones': calificaciones
    })