from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# здесь хранятся все действующие ссылки на сайте(к каждому пути привязана своя функция, которая находится
# в файле views.py
urlpatterns = [
                  path('', views.main, name='main'),

                  path('post/<int:id>/', views.detail_post, name='detail-view'),
                  path('edit-post/<int:id>/', views.edit_post, name='edit-post'),
                  path('delete/<int:id>/', views.deletepost, name='delete'),
                  path('create', views.create_post, name='createpost'),

                  path('delete-account/', views.deleteaccount, name='delete-account'),
                  path('sign/up', views.registration, name='registration'),
                  path('sign/in', views.login, name='login'),
                  path('sign/out', views.logout, name='logout'),
                  path('user/<int:id>/', views.detail_user, name='detail-user'),


                  path('searchresult/', views.search_result, name='searchresult')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
