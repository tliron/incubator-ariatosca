
import platform

class get_architecture(object):
    def __call__(self):
        return platform.machine()

class get_type(object):
    def __call__(self):
        return platform.system().lower()

class get_distribution(object):
    def __call__(self):
        return platform.dist()[0].lower()

class get_version(object):
    def __call__(self):
        return platform.dist()[1]
