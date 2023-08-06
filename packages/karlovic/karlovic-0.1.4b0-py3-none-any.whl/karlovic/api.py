import bottle
import base64
from karlovic.request_logger import log


def default_routes(app):
    @app.route('/<:re:.*>', method="OPTIONS")
    def options():
        bottle.response.status = 204
        return {}

    @app.get('/v1/health')
    def health():
        return {
            'status': 'ok',
        }

    @app.get('/favicon.ico')
    def favicon():
        favicon = base64.b64decode((
            'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/'
            'xhBQAAADhlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAAqACAAQAAAABA'
            'AAAEKADAAQAAAABAAAAEAAAAAAXnVPIAAACF0lEQVQ4EaVTTWgTQRT+ZjfJNm3a/'
            'EloJXhRsReLpChYVHpVD1IEwYvgRYtHERTqpdSbPQgFhR60goKgHqQXLx69CEKpUILYg1Yx/'
            '6ZJdzdJs9m+eetOU5pbF2bm7Xvv+2be+2bE8dNTLg7waQfAMjTQiyCgaziUjCHSH0JfKIi24'
            '8ButrFlNmBaDTSaLQXbR5CIRXDl4gVM37wGg8CqPjJKlSpevlnGq7cfFcGeEkZScczev4W7d'
            '24gHhtCrlDGWvYH2m0HAwNhHEkPIzM2qsDSUCfoDxuYfTCNc2cz0DUNz19/wPvlT8jli3h47'
            'zamLk9CCIH6lt2b4MTRNM5PjDN45VsWz168o2QLnY5Lo8Mgh3pRqdZ6E1y/eonBMrq6to7'
            'NmsmJGu2aPpxi27KbKJX/se1Pqgen/tdmWjZ+/c75cV6HU0leLbvBfekOKoIENU1+29tSr'
            't06g0EdseggxwrFErLf19n2J0Xgup5ghhFCIu4BZJImXBqC8+t1k5vqg+WqVNj4k0d0KIJwn'
            '4HJiQy+rmTRbLUweiyNQNBLc6ihpCiE2raLYH5hCUtP55j8zPhJLD6ZYf2T8ajasEOnFJqu/'
            'qWhuD5/WcXMowUUihVOiA5GUC5XMfd4EdXNOhySUsroup6kPovY+xpdum0jVEaIEoEa1Zwv'
            'ltmn0/uwSCF5O6kIH7/bA88j9kko/T83/ipAN1g6dwDWGr9H4vfiUQAAAABJRU5ErkJggg=='
        ))
        bottle.response.content_type = 'image/x-icon'
        return favicon
