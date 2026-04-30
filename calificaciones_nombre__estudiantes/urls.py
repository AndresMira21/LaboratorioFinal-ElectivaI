from django.urls import path
from . import views

urlpatterns = [

    # ── Autenticación ─────────────────────
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ── CRUD Calificaciones ───────────────
    path('', views.listar, name='listar'),
    path('crear/', views.crear, name='crear'),
    path('editar/<int:pk>/', views.editar, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar, name='eliminar'),

    # ── Promedio general ──────────────────
    path('promedio-general/', views.promedio_general, name='promedio_general'),
]