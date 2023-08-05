import posixpath

from importlib.util import find_spec
from pathlib import Path

from django.conf import settings

from django.http import Http404
from django.views import static


def serve(request, path, **kwargs):
    if settings.DEBUG is False and getattr(settings, 'BRYTHON_UNITTEST_RUNNING', False) is False:
        raise Http404(f'To access brython files from server please set DEBUG or BRYTHON_UNITTEST_RUNNING to True')

    module_path = posixpath.normpath(path).lstrip('/').replace('.py', '').replace('/', '.')

    if module_path == 'django_brython.testing':
        module_path = 'django_brython.mock_testing'

    try:
        module = find_spec(module_path)
    except ModuleNotFoundError:
        raise Http404(f"'import {module_path}' exception, file: {path} can't be served")

    if not module:
        raise Http404(f"'import {module_path}' exception, file: {path} can't be served")

    tested_module_path = Path(module.origin)

    if not str(tested_module_path).endswith(path) and module_path != 'django_brython.mock_testing':
        raise Http404(f"Requested and imported module doesn't match. Imported: {module.origin}, requested: {path}")

    return static.serve(request, tested_module_path.name, document_root=tested_module_path.parent, **kwargs)
