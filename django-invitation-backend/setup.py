import os
import sys
from distutils.core import setup
from invitation import get_version, __maintainer__, __email__


def compile_translations():
    try:
        from django.core.management.commands.compilemessages \
                                                       import compile_messages
    except ImportError:
        return None
    curdir = os.getcwdu()
    os.chdir(os.path.join(os.path.dirname(__file__), 'invitation'))
    try:
        compile_messages(stderr=sys.stderr)
    except TypeError:
        # compile_messages doesn't accept stderr parameter prior to 1.2.4
        compile_messages()
    os.chdir(curdir)
compile_translations()


long_description = open('README.rst').read()


setup(
    name = 'django-invitation-backend',
    version = get_version().replace(' ', '-'),
    url = 'http://github.com/volrath/django-invitation-backend',
    author = __maintainer__,
    author_email = __email__,
    license = 'BSD',
    packages = ['invitation',
                'invitation.tests'],
    package_data= {
        'invitation': ['tests/templates/invitation/*',
                       'tests/templates/registration/*',
                       'locale/*/LC_MESSAGES/django.*']
    },
    data_files=[('', ['LICENSE.txt',
                      'README.rst'])],
    description = 'Registration through invitations backend for django-registration > 0.9',
    long_description=long_description,
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content']
)
