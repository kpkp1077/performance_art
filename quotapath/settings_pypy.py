"""
PyPy-optimized Django settings for quotapath project.
"""

from .settings import *
import os
import sys

# PyPy-specific optimizations
if hasattr(sys, 'pypy_version_info'):
    # Database connection pooling optimizations for PyPy
    DATABASES['default'].update({
        'CONN_MAX_AGE': 60,  # Reuse connections for 60 seconds
        'OPTIONS': {
            'MAX_CONNS': 20,
            'MIN_CONNS': 5,
        }
    })
    
    # Cache optimizations for PyPy
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': config('REDIS_URL', default='redis://localhost:6379'),
            'OPTIONS': {
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 50,
                    'retry_on_timeout': True,
                }
            }
        }
    }
    
    # Session optimizations
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
    
    # PyPy-optimized middleware order
    MIDDLEWARE = [
        'django.middleware.cache.UpdateCacheMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware',
    ]
    
    # Cache settings for PyPy
    CACHE_MIDDLEWARE_ALIAS = 'default'
    CACHE_MIDDLEWARE_SECONDS = 300
    CACHE_MIDDLEWARE_KEY_PREFIX = 'quotapath'

# PyPy garbage collection hints
import gc
if hasattr(sys, 'pypy_version_info'):
    # Configure PyPy GC for Django
    gc.set_threshold(700, 10, 10)  # More aggressive collection for web apps