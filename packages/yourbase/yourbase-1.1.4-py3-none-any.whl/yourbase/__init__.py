import atexit
import inspect
import os

from logging import DEBUG, Formatter, getLogger, INFO, Logger, Handler, StreamHandler

logger: Logger = getLogger("yourbase-python")
handler: Handler = StreamHandler()
handler.setFormatter(Formatter("[YB] %(message)s"))
logger.addHandler(handler)

if os.getenv("YB_DEBUG", "false") == "true":
    logger.setLevel(DEBUG)
else:
    logger.setLevel(INFO)

# yourbase.pytest does not need to be imported here; it is loaded via our
# setup.py -> entry_points dict

CTX = None
ENABLED = False
PLUGIN = None


def shutdown_acceleration(self, *args, **kwargs):
    if CTX and PLUGIN:
        logger.info("Processing acceleration data")
        PLUGIN.dump_graph()
        CTX.stop()


try:
    import yourbase_plugin

    if yourbase_plugin.AVAILABLE:
        ENABLED = True
        from coverage import Coverage
        from coverage.config import CoverageConfig

        CTX = Coverage()
        cconf = CoverageConfig()
        cconf.data_file = None
        CTX.set_option("run:plugins", ["yourbase_plugin"])
        logger.info("Starting Python acceleration engine")
        CTX.start()
        PLUGIN = CTX._plugins.get("yourbase_plugin.YourBasePlugin")
        atexit.register(shutdown_acceleration, None, None)

except Exception as e:
    logger.info("Not running on YourBase CI, build won't be accelerated")
    logger.debug(f"  because {e}")


def skip_when_possible(func):
    def wrapper(*args, **kwargs):
        if PLUGIN is None:
            func(*args, **kwargs)
        else:
            fname = "%s" % (func.__qualname__)
            fpath = os.getcwd() + os.sep + inspect.getfile(func)
            if PLUGIN.can_skip(fpath, fname):
                logger.info("Skipping %s (@ %s)" % (fname, fpath))
            else:
                PLUGIN.start_test(fpath, fname)
                func(*args, **kwargs)
                PLUGIN.end_test(fpath, fname)

    return wrapper


def accelerate_tests():
    class ClassWrapper:
        def __init__(self, cls):
            self.other_class = cls

        def __call__(self, *cls_ars):
            other = self.other_class(*cls_ars)
            funcs = inspect.getmembers(self.other_class, predicate=inspect.isfunction)
            for fn in funcs:
                f = fn[0]
                if callable(getattr(other, f)):
                    setattr(other, f, skip_when_possible(getattr(other, f)))
            return other

    return ClassWrapper
