from django.conf.urls import url
from django.contrib import admin
from app import views

urlpatterns = [
    # Django admin URL
    url(r'^admin/', admin.site.urls),

    # Application URLs
    url(r'^$', views.login, name='login'),
    url(r'^test/$', views.test, name='test'),
    url(r'^save/$', views.save, name='save'),
    url(r'^results/$', views.results, name='results'),
]
