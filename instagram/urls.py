from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns = [
     url('^$',views.welcome,name = 'home'),
     url(r'^instagram/profile$',views.profile,name='displayProfile'),
     url(r'^images',views.image,name="images"),
     url(r'^instagram/prof/(\d+)',views.prof,name="prof"),
     url(r'^instagram/comments/(\d+)',views.comments,name="comments"),
     url(r'^instagram/comm/(\d+)',views.comm,name="comm")
   
     
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)