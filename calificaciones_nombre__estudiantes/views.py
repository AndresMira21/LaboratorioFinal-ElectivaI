
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Avg
from .models import Calificacion
from .forms import CalificacionForm, RegistroUsuarioForm

# ─────────────────────────────────────────
# AUTENTICACIÓN
# ─────────────────────────────────────────

def registro(request):
    """
    Vista para registrar nuevos usuarios.
    GET → muestra el formulario de registro vacío.
    POST → crea el usuario y redirige al login.
    """
    if request.user.is_authenticated:
        return redirect('listar')
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}! Cuenta creada exitosamente.')
            return redirect('listar')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'calificaciones/registro.html', {'form': form})


def login_view(request):
    """
    Vista de inicio de sesión.
    Usa el AuthenticationForm de Django que valida usuario y contraseña.
    Si es correcto, inicia la sesión y redirige.
    """
    if request.user.is_authenticated:
        return redirect('listar')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}!')
            return redirect('listar')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'calificaciones/login.html', {'form': form})


def logout_view(request):
    """
    Cierra la sesión del usuario y redirige al login.
    """
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('login')


# ─────────────────────────────────────────
# CRUD CALIFICACIONES
# ─────────────────────────────────────────

@login_required
def listar(request):
    """
    Muestra todas las calificaciones.
    Calcula el promedio general usando Avg de Django.
    @login_required redirige al login si el usuario no está autenticado.
    """
    calificaciones = Calificacion.objects.all()

    # Calcula el promedio general de todos los registros
    promedio_general = Calificacion.objects.all().aggregate(
        Avg('promedio')
    )['promedio__avg']

    # Redondea a 2 decimales si hay datos, si no muestra 0
    if promedio_general:
        promedio_general = round(promedio_general, 2)
    else:
        promedio_general = 0

    return render(request, 'calificaciones/listar.html', {
        'calificaciones': calificaciones,
        'promedio_general': promedio_general,
        'total': calificaciones.count()
    })


@login_required
def crear(request):
    """
    Crea una nueva calificación.
    El promedio se calcula automáticamente en el modelo (save).
    """
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            form.save()   # aquí se llama al save() del modelo que calcula el promedio
            messages.success(request, 'Calificación registrada exitosamente.')
            return redirect('listar')
    else:
        form = CalificacionForm()
    return render(request, 'calificaciones/crear.html', {'form': form})


@login_required
def editar(request, pk):
    """
    Edita una calificación existente.
    instance=calificacion le dice al formulario que está editando, no creando.
    Al guardar, el promedio se recalcula automáticamente.
    """
    calificacion = get_object_or_404(Calificacion, pk=pk)
    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Calificación actualizada exitosamente.')
            return redirect('listar')
    else:
        form = CalificacionForm(instance=calificacion)
    return render(request, 'calificaciones/editar.html', {
        'form': form,
        'calificacion': calificacion
    })


@login_required
def eliminar(request, pk):
    """
    Elimina una calificación.
    GET → muestra confirmación.
    POST → ejecuta la eliminación.
    """
    calificacion = get_object_or_404(Calificacion, pk=pk)
    if request.method == 'POST':
        calificacion.delete()
        messages.success(request, 'Calificación eliminada exitosamente.')
        return redirect('listar')
    return render(request, 'calificaciones/eliminar.html', {
        'calificacion': calificacion
    })


@login_required
def promedio_general(request):
    """
    Vista dedicada al promedio general.
    Usa Avg de Django para calcular el promedio de todos los promedios.
    También muestra estadísticas adicionales.
    """
    total = Calificacion.objects.count()
    promedio = Calificacion.objects.aggregate(Avg('promedio'))['promedio__avg']

    if promedio:
        promedio = round(promedio, 2)
    else:
        promedio = 0

    # Estadísticas adicionales
    aprobados = Calificacion.objects.filter(promedio__gte=3.0).count()
    reprobados = Calificacion.objects.filter(promedio__lt=3.0).count()

    # Top 5 mejores estudiantes
    top_estudiantes = Calificacion.objects.order_by('-promedio')[:5]

    return render(request, 'calificaciones/promedio_general.html', {
        'promedio_general': promedio,
        'total': total,
        'aprobados': aprobados,
        'reprobados': reprobados,
        'top_estudiantes': top_estudiantes

    })
