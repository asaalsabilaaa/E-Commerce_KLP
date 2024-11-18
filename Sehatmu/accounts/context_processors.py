import os
from django.conf import settings

def versioned_static(request):
    version = 'v1.1'  # Ubah versi ini saat ada perubahan file statis
    return {
        'STATIC_VERSION': version,
    }
