from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Root URL
    path('final_report/', views.final_report_view, name='final_report'),
    path('fetch-data/', views.fetch_data, name='fetch_data'),
    path('update-revised-estimate/', views.update_revised_estimate, name='update_revised_estimate'),
    path('add/', views.add_data, name='add_data'),  # New URL for adding data
    path("import_csv/", views.import_csv, name="import_csv"),
    
    path('supplementary_report/', views.supplementary_report_view, name='supplementary_report'),
    path('fetch-supplementary-data/', views.fetch_supplementary_data, name='fetch_supplementary_data'),
    path('changes_report/', views.revision_report_view, name='revision_report'),
    path('fetch-revision-data/', views.fetch_revision_data, name='fetch_revision_data'),
]
