from django.db import models

# Create your models here.
class GDP(models.Model):
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=4)
    year = models.PositiveSmallIntegerField()
    gdp = models.FloatField()

    def __str__(self):
        return self.country