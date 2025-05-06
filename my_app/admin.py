from django.contrib import admin
from .models import Monkey, Feeding, Toy

# Register your models here.
admin.site.register(Monkey)
admin.site.register(Feeding)
admin.site.register(Toy)