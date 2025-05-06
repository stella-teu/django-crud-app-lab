from django.db import models

MEALS = ( ('F', 'Fruits'), ('N', 'Nuts'), ('L', 'Leaves'))
SIZES = ( ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'))

# Create your models here.
class Toy(models.Model):
    name = models.CharField(max_length=50)
    size = models.CharField(max_length=1, choices=SIZES, default=SIZES[0][0])
    
    def __str__(self):
        return self.name

class  Monkey(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)
    
    def __str__(self):
        return self.name

class Feeding(models.Model):
    monkey = models.ForeignKey(Monkey, on_delete=models.CASCADE)
    date = models.DateField()
    meals = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
    
    def __str__(self):
        return f'{self.get_meals_display()} on {self.date}'
    
    class Meta:
        ordering = ['-date']