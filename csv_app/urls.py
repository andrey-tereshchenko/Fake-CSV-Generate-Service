from django.urls import path
from csv_app import views

urlpatterns = [
    path('create/', views.SchemaCreateView.as_view(), name='create_schema'),
    path('generate_dataset/', views.DataSetCreateView.as_view(), name='create_dataset'),
    path('dataset_list/', views.DataSetListView.as_view(), name='dataset_list'),
    path('list/', views.SchemaListView.as_view(), name='schemas_list'),
    path('<pk>/update', views.SchemaUpdateView.as_view(), name='update_schema'),
    path('<pk>/delete', views.SchemaDeleteView.as_view(), name='delete_schema'),
    path('dataset/<pk>/delete', views.DataSetDeleteView.as_view(), name='delete_dataset'),
    path('download/<path:path>', views.download, name='download'),
]
