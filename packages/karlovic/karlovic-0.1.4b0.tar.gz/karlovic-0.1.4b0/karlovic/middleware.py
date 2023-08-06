import bottle


@bottle.hook('before_request')
def strip_path():
    bottle.request.environ['PATH_INFO'] = bottle.request.environ['PATH_INFO'].rstrip(
        '/')


def use_middleware(app):
    def apply_header(response, header):
        response.headers[header[0]] = header[1]

    @app.hook('after_request')
    def cors():
        cors_headers = [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-control-Allow-Methods', (
                'GET, POST, PUT, OPTIONS'
            )),
            ('Access-Control-Allow-Headers', (
                'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
            ))
        ]
        for header in cors_headers:
            apply_header(bottle.response, header)
