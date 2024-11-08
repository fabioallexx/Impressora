from django.db import models

class Leitor(models.Model):
    numero_leitor = models.IntegerField(db_column='NumeroLeitor', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=255)
    apelido = models.CharField(db_column='Apelido', max_length=255)

    class Meta:
        db_table = 'Leitor'
        managed = False