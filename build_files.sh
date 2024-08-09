

pip install -r requirements.txt 
python3.9 manage.py collectstatic


settings.py

ALLOWED_HOSTS = ['.vercel.app','now.sh','127.0.0.1','localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'WalletWatch',
        'USER': 'postgres',
        'PASSWORD': 'nandan38',
        'HOST': '',
        'PORT': '5432',
    }
}

STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

urls.py

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
