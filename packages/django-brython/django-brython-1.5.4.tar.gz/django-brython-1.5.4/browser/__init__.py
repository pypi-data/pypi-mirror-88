

class BrythonLibMock:
    def __getattribute__(self, item):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __le__(self, other):
        pass

    def __ge__(self, other):
        pass


aio = BrythonLibMock()
ajax = BrythonLibMock()
html = BrythonLibMock()
local_storage = BrythonLibMock()
markdown = BrythonLibMock()
object_storage = BrythonLibMock()
session_storage = BrythonLibMock()
svg = BrythonLibMock()
template = BrythonLibMock()
timer = BrythonLibMock()
webcomponent = BrythonLibMock()
websocket = BrythonLibMock()
worker = BrythonLibMock()
widgets = BrythonLibMock()

document = BrythonLibMock()
window = BrythonLibMock()
