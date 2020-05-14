from django.contrib import admin

# Register your models here.
from book import models

admin.site.register(models.Books)
admin.site.register(models.Press)
admin.site.register(models.Author)
admin.site.register(models.AuthorDetail)
