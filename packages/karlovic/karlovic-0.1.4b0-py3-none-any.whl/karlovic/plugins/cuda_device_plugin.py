from karlovic.plugins.ensure_nonconflicting_plugins import ensure_nonconflicting_plugins
from karlovic.plugins.get_plugin_value import get_plugin_value


class CudaDevicePlugin:
    name = 'device'
    api = 2

    def __init__(self, device, keyword='device'):
        self.keyword = keyword
        self.device = device

    def setup(self, app):
        ensure_nonconflicting_plugins(self, app)

    def apply(self, f, context):
        @get_plugin_value(f, context, self.keyword)
        def _f():
            return self.device

        return _f
