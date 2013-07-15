import os
import sys
sys.path.append('/home/rrix/dev/mbrace')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mbrace.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import djcelery
djcelery.setup_loader()

