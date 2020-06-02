from django.db import models
from django.contrib.auth.models import User

class Printers(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машини'
        ordering = ['name']

class RipLog(models.Model):
    printer = models.ForeignKey('machinelog.Printers', blank=False, null=False, related_name="log_printers", on_delete=models.CASCADE)
    status = models.IntegerField("Статус", null=True, default=None)
    work_name = models.CharField("Макет", max_length=256)
    width = models.FloatField("Ширина", null=True)
    height = models.FloatField("Висота", null=True)
    count = models.IntegerField("Кількість", null=True, default=False)
    datetime = models.DateTimeField("Дата/Час", auto_now=False, auto_now_add=False)
    timestamp = models.IntegerField("Штамп", null=True, default=False)

    def __str__(self):
        return self.work_name

    class Meta:
        verbose_name = 'RIP Лог'
        verbose_name_plural = 'RIP Логи'
        ordering = ['datetime']

class PrintLog(models.Model):
    printer = models.ForeignKey('machinelog.Printers', blank=False, null=False, related_name="rip_printers", on_delete=models.CASCADE)
    start = models.DateTimeField("Дата початку", auto_now=False, auto_now_add=False)
    work_name = models.CharField("Макет", max_length=256)
    duration = models.TimeField("Тривалість", auto_now=False, auto_now_add=False)
    percentage = models.IntegerField("%", null=True, default=False)
    m_kv = models.DecimalField("м.кв.", max_digits=9, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.work_name

    class Meta:
        verbose_name = 'Print Лог'
        verbose_name_plural = 'Print Логи'
        ordering = ['start']
