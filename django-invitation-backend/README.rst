Built on top of ``django-registration``, **django-invitation-backend**
handles registration through invitations.

.. note::
   This backend is built for ``django-registration 0.9`` or above.


Features
========

- Invitations can be optional or required to be registered.
- Admin integration


Installation
============

This application depends on ``django-registration``.

#. Add ``"django-invitation-backend"`` directory to your Python path.
#. Add ``"invitation"`` to your ``INSTALLED_APPS`` tuple found in your
   settings file.
#. Include ``"invitation.urls"`` to your URLconf.


Testing & Example
=================

TODO


Usage
=====

You can configure ``django-invitation-backend`` app's behaviour with
the following settings:

:INVITATION_INVITE_ONLY:
    Set this to True if you want registration to be only possible via
    invitations. Default value is ``False``.

:INVITATION_EXPIRE_DAYS:
    How many days before an invitation is expired. Default value is ``15``.


See Also
========

-  `django-inviting <http://https://github.com/muhuk/django-inviting>`_
