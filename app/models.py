from django.db import models
from django.contrib.auth.models import User


class LogAcesso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criada_em']  # ultimo acesso primeiro
