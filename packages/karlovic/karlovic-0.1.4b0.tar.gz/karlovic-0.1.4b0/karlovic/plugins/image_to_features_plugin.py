from karlovic.plugins.ensure_nonconflicting_plugins import ensure_nonconflicting_plugins
from karlovic.plugins.get_plugin_value import get_plugin_value


class ImageToFeaturesPlugin:
    name = 'image_to_features'
    api = 2

    def __init__(self, config, architecture, keyword='image_to_features'):
        self.config = config

        self.keyword = keyword
        self.architecture = architecture

    def setup(self, app):
        ensure_nonconflicting_plugins(self, app)

    def image_to_features(self, image):
        return self.architecture.FeatureBatch.from_images([image])

    def apply(self, f, context):
        @get_plugin_value(f, context, self.keyword)
        def _f():
            return self.image_to_features

        return _f
