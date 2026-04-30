from django.db import models

class Calificacion(models.Model):
    nombre_estudiante = models.CharField(max_length=150)
    identificacion = models.CharField(max_length=15)
    asignatura = models.CharField(max_length=100)
    nota1 = models.DecimalField(max_digits=5, decimal_places=2)
    nota2 = models.DecimalField(max_digits=5, decimal_places=2)
    nota3 = models.DecimalField(max_digits=5, decimal_places=2)
    promedio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        editable=False,   # ← no aparece en el formulario
        default=0
    )

    def calcular_promedio(self):
        """
        Calcula el promedio de las tres notas.
        Se redondea a 2 decimales.
        """
        return round((self.nota1 + self.nota2 + self.nota3) / 3, 2)

    def save(self, *args, **kwargs):
        """
        Sobreescribe el método save para calcular
        el promedio automáticamente antes de guardar.
        Siempre que se crea o edita un registro,
        el promedio se recalcula solo.
        """
        self.promedio = self.calcular_promedio()
        super().save(*args, **kwargs)

    def estado(self):
        """
        Devuelve el estado del estudiante según su promedio.
        """
        if self.promedio >= 3.0:
            return 'Aprobado'
        return 'Reprobado'

    def _str_(self):
        return f"{self.nombre_estudiante} - {self.asignatura} - {self.promedio}"

    class Meta:
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        ordering = ['nombre_estudiante']