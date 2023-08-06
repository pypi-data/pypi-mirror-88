from django.utils.translation import ugettext_lazy as _

from fperms.enums import *


PERM_TYPE_CORE = 'is_core'

IS_CORE_PERM_TYPE_CHOICES = (
    (PERM_TYPE_CORE, _('IS core')),
)

PERM_TYPE_CHOICES = settings.PERM_TYPE_CHOICES + IS_CORE_PERM_TYPE_CHOICES

PERM_CODENAME_CREATE = 'create'
PERM_CODENAME_READ = 'read'

PERM_CODENAMES.update({
    PERM_CODENAME_CREATE: _('create'),
    PERM_CODENAME_READ: _('read'),
})
