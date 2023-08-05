# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rest_captcha']

package_data = \
{'': ['*'], 'rest_captcha': ['fonts/*']}

install_requires = \
['Pillow>=4.3.0', 'django', 'djangorestframework>=3.5,<4.0']

setup_kwargs = {
    'name': 'django-rest-captcha',
    'version': '0.2.0',
    'description': 'Lightweight version of django-simple-captcha for work with django-rest-framework',
    'long_description': "# Django rest captcha\n\nLightweight version of `django-simple-captcha` for work with `django-rest-framework`.\n\n\n## Features\n\n- Speed: use `cache` instead of database\n- Safety: union methods for generate key and image. (You can't generate many images for one key)\n- Easy: only one rest api (for generate, refresh image).\n\n\n## Usage\nAdd `RestCaptchaSerializer` to your protected request validator:\n```\nfrom rest_captcha serializer import RestCaptchaSerializer\nclass HumanOnlyDataSerializer(RestCaptchaSerializer):\n    pass\n```\nThis code add to your serializer two required fields (captcha_key, captcha_value)\n\n\nFor provide this fields client(js code) should generate key:\n```\n> curl -X POST http:localhost:8000/api/captcha/ | python -m json.tool\n{\n    'image_type': 'image/png',\n    'image_decode': 'base64',\n    'captcha_key': 'de67e7f3-72d9-42d8-9677-ea381610363d',\n    'captcha_value': '... image encoded in base64'\n}\n```\n`captcha_value` - is base64 encoded PNG image, client should decode and show this image to human for validation and send letters from captcha to protected api.\nIf human have mistake - client should re generate your image.\n\n**Note:** See also [trottling](https://www.django-rest-framework.org/api-guide/throttling/) for protect public api\n\n\n## Install\n```\n> pip install django-rest-captcha\n```\n\n### Add to your settings.py\nAdd to installed apps:\n```\nINSTALLED_APPS = (\n    ...\n    'rest_captcha',\n)\n```\n\nSet rest_captcha settings (if you want), see defaults:\n```\nREST_CAPTCHA = {\n    'CAPTCHA_CACHE': 'default',\n    'CAPTCHA_TIMEOUT': 300,  # 5 minutes\n    'CAPTCHA_LENGTH': 4,\n    'CAPTCHA_FONT_SIZE': 22,\n    'CAPTCHA_IMAGE_SIZE': (90, 40),\n    'CAPTCHA_LETTER_ROTATION': (-35, 35),\n    'CAPTCHA_FOREGROUND_COLOR': '#001100',\n    'CAPTCHA_BACKGROUND_COLOR': '#ffffff',\n    'CAPTCHA_FONT_PATH': FONT_PATH,\n    'CAPTCHA_CACHE_KEY': 'rest_captcha_{key}.{version}',\n    'FILTER_FUNCTION': 'rest_captcha.captcha.filter_default',\n    'NOISE_FUNCTION': 'rest_captcha.captcha.noise_default'\n}\n```\n\nWe recommend using redis or local memory as cache with set parameter, with bigger value of MAX_ENTRIES:\n```\nCACHES={\n    'default': {\n        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',\n        'LOCATION': 'rest-captcha',\n        'MAX_ENTRIES': 10000,\n    }\n}\n```\n\n### Add hooks to your app router (urls.py):\n```\nurlpatterns = [\n    ...\n    url(r'api/captcha/', include('rest_captcha.urls')),\n]\n```\n",
    'author': 'evgeny.zuev',
    'author_email': 'zueves@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
