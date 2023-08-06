=============================
django-fperms-iscore
=============================

.. image:: https://badge.fury.io/py/django-fperms-iscore.svg
    :target: https://badge.fury.io/py/django-fperms-iscore

.. image:: https://travis-ci.org/Formulka/django-fperms-iscore.svg?branch=master
    :target: https://travis-ci.org/druids/django-fperms-iscore

.. image:: https://codecov.io/gh/Formulka/django-fperms-iscore/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/druids/django-fperms-iscore

Perms for iscore library

Documentation
-------------

The full documentation is at https://django-perms-iscore.readthedocs.io.


Quickstart
----------

Install django-fperms-iscore::

    pip install django-fperms-iscore

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'fperms_iscore.apps.FPermsConfig',
        ...
    )


It includes all the basic permissions from http://github.com/formulka/django-fperms and adds a new type:

- **core**: for iscore specific resources

Usage
-----

A superuser has for all intents and purposes permission to do everything. For regular users you can assign permissions directly or via a user group.

**Creating a new permission**:

You can create a new permission directly via its model or via a specially formated string:

.. code-block:: python

    from fperms_iscore import enums
    from fperms_iscore.models import IsCorePerm

    IsCorePerm.objects.create(
        type=enums.PERM_TYPE_CORE,
        codename='create',
        core='issue_tracker.IssueIsCore',
    )
    IsCorePerm.objects.create_from_str('core.issue_tracker.IssueIsCore.create')

**Assigning a permission**:

You can assign existing permission via the custom ``perms`` manager available for both User (including custom ones) and Group models. You can add single permission or multiple both directly via its instance or using the formated string:

.. code-block:: python

    from django.auth.models import User, Group

    from fperms_iscore.models import IsCorePerm

    perm = IsCorePerm.objects.create_from_str('core.issue_tracker.IssueIsCore.create')

    user = User.objects.get(pk=1)
    user.perms.add_perm(perm)

    group = Group.objects.get(pk=1)
    group.perms.add_perm('core.issue_tracker.IssueIsCore.create')

By default if said permission does not exist, it will raise an exception. You can override this behavior by setting ``PERM_AUTO_CREATE`` variable in your project settings to ``True``, assigning a permission will then create it as well if it does not exist.

**Retrieving permission instance**:

You can get a permission instance directly from the model or via the string representation.

.. code-block:: python

    perm = IsCorePerm.objects.get(
        type=enums.PERM_TYPE_CORE,
        codename='create',
        core='issue_tracker.IssueIsCore',
    )
    perm = IsCorePerm.objects.get_from_str('core.issue_tracker.IssueIsCore.create')

**Checking permission**:

You can check whether the user or group has a required permission via ``has_perm`` method of the ``perms`` manager again using both the permission instance or the string representation.

.. code-block:: python

    ...
    perm = IsCorePerm.objects.create(
        type=enums.PERM_TYPE_CORE,
        codename='create',
        core='issue_tracker.IssueIsCore',
    )

    assert user.perms.has_perm(perm)
    assert user.perms.has_perm('core.issue_tracker.IssueIsCore.create')

New perm type
-------------------

**core**

- permission for iscore specific resources
- type is defined as ``fperms_iscore.enums.PERM_TYPE_CORE``
- codename is usually one of the CRUD operations (create, read, update, delete)
- it requires ``type``, ``codename`` and ``core`` fields
- string representation is ``'core.<app_label>.<core_name>.<codename>'``

.. code-block:: python

    ...
    # equivalent results:
    IsCorePerm.objects.create(
        type=enums.PERM_TYPE_CORE,
        codename='create',
        core='issue_tracker.IssueIsCore',
    )
    IsCorePerm.objects.create_from_str('core.issue_tracker.IssueIsCore.create')

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
