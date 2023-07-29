from django.contrib import admin

# Register your models here.
from documents.models import documents, usersCerts

admin.site.register(documents)
admin.site.register(usersCerts)
