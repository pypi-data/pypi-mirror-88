# drf_simplepermissions

This is a simple class to handle permissions in a Django application. It allows
you to list permissions as a tuple, list or string without writing custom
classes for each exception.

# Usage

```python
from drf_simplepermissions import SimplePermissions
from rest_framework import generics


class SimpleView(generics.GenericAPIView):
  serializer_class = ...
  permission_classes = (SimplePermissions,)
  allowed_permissions = ('codename_x', 'codename_y')

  def get(self, request, format=None):
    ...
```

It also includes a simple `is_demo()`-method which can be used to check if
views or other methods should be running in demo mode.

```python
from drf_simplepermissions import is_demo

if is_demo(User):
  # We should run in demo mode when the user is in 'demo'
```

# Settings

Settings can be managed in `settings.py`.

## DEMO

Global demo mode can be enabled by changing `settings.DEMO` to True. If
it's set to False you can override it by adding users to a group. You
can't override `settings.DEMO` when it's set to True. When global demo
mode is set to true, all users no matter their group membership will be
considered demo users.

## DEMO_GROUPS

`settings.DEMO_GROUPS` contains a string or a list of groups that should be
considered demo users. It will try to match against any group and if a match
is found, it will return true. It is set to 'demo' by default. Groups are
not managed by this module and should be added manually or with a custom
migration.

# Installation

Not documented yet.
