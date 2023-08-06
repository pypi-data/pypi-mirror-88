import bottle


def ensure_nonconflicting_plugins(self, app):
    for other in set(app.plugins) - {self}:
        if hasattr(other, 'keyword') and self.keyword == other.keyword:
            raise bottle.PluginError(
                'Found another plugin with conflicting keyword'
            )
