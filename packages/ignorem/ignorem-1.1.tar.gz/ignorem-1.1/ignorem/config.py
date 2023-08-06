import os
import simplecfg

_config = simplecfg.Config(os.path.join(simplecfg.dir.APP_DATA, "ignorem"), "config")


def get(key):
	return _config.get(key)


def store(key, value):
	_config.set(key, value)
