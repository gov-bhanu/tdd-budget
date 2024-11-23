from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Root URL
    path('fetch-data/', views.fetch_data, name='fetch_data'),
    path('update-revised-estimate/', views.update_revised_estimate, name='update_revised_estimate'),
    path('add/', views.add_data, name='add_data'),  # New URL for adding data
    path("import_csv/", views.import_csv, name="import_csv"),


]
