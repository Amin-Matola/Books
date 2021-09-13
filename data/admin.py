from django.contrib import admin
from .models import Users,Book,Download,Vistor

#--------------------------------------------------------------
#------------------- Registering models in admin page----------|
#--------------------------------------------------------------


admin.site.register(Users)
admin.site.register(Book)
admin.site.register(Download)
admin.site.register(Vistor)
