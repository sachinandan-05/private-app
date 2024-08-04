"""private_info URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib import admin
from django.views.static import serve
from Private.models import Private_SubModel
from django.shortcuts import redirect
from django.contrib import messages


def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            user2 = request.session.get('private_admin')
            link = request.path.split('uploads/')[1]
            check = Private_SubModel.objects.get(private_img=link)
            if user2 or check.private_id.share == True:
                if str(check.private_id.user.username).lower() == str(user2).lower()  or check.private_id.share == True:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, 'You are not allowed to view this page')
                    return redirect('/view/')
            else:
                messages.error(request, 'You are not allowed to view this page')
                return redirect('/login/')
        except:
            messages.error(request, 'You are not allowed to view this page')
            return redirect('/view/')

    return wrapper


@custom_login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Private.urls')),
    path('', include('User.urls')),
    re_path(r'^uploads/(?P<path>.*)$', protected_serve, {'document_root': settings.MEDIA_ROOT}),
]

handler404 = "Private.views.page_not_found_view"
