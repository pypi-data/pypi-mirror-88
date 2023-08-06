from karlovic.plugins.ensure_nonconflicting_plugins import ensure_nonconflicting_plugins
from karlovic.plugins.get_plugin_value import get_plugin_value
import bottle
import base64
import binascii
from PIL import Image
import io


class ImagePlugin:
    name = 'image'
    api = 2

    def __init__(self, keyword='image'):
        self.keyword = keyword

    def setup(self, app):
        ensure_nonconflicting_plugins(self, app)

    def apply(self, f, context):
        @get_plugin_value(f, context, self.keyword)
        def _f():
            content_type = bottle.request.content_type
            if content_type == 'application/json':
                data = bottle.request.json.get('image')
                if data is None:
                    bottle.abort(400, 'Value \'image\' missing')
                try:
                    decoded_data = base64.b64decode(data, validate=True)
                except binascii.Error:
                    bottle.abort(415, 'base64 decode failed')

                file_ = io.BytesIO(decoded_data)
            elif content_type.split(';')[0] == 'multipart/form-data':
                try:
                    image = bottle.request.files.get('image')
                    file_ = image.file
                except (KeyError, AttributeError):
                    bottle.abort(400, 'Form field \'image\' missing')
                except UnicodeError:
                    bottle.abort(400, '\'image\' not Unicode')

            else:
                bottle.abort(415, (
                    f'Content-Type: {content_type} not supported'
                    ' (only application/json and multipart/form-data)'
                ))

            try:
                image = Image.open(file_).convert('RGB')
            except Exception:
                bottle.abort(
                    415, 'Image format not supported or image data corrupt')

            return image

        return _f
