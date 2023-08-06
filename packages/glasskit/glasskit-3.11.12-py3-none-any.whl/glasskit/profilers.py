import cProfile
import mtprof
import io
import pstats
import functools
import warnings

try:
    import line_profiler
except ImportError:
    warnings.warn("Could not import line_profiler. Line profiling is disabled")
    line_profiler = None

from . import ctx

from flask import g
from datetime import datetime


def before_request():
    from .api import get_boolean_request_param

    if get_boolean_request_param("profile"):
        if line_profiler and ctx.line_profiler.functions:
            g.line_profiler = line_profiler.LineProfiler(*ctx.line_profiler.functions)
            g.line_profiler.enable()
        if get_boolean_request_param("profile_threads"):
            g.profiler = mtprof.Profile()
        else:
            g.profiler = cProfile.Profile()
        g.profiler.enable()


def after_request(response):
    if hasattr(g, "profiler"):
        g.profiler.disable()
        strio = io.StringIO()
        ps = pstats.Stats(g.profiler, stream=strio).sort_stats("cumulative")
        ps.print_stats()
        ctx.log.debug(strio.getvalue())

    if hasattr(g, "line_profiler"):
        g.line_profiler.disable()
        strio = io.StringIO()
        g.line_profiler.print_stats(stream=strio)
        ctx.log.debug(strio.getvalue())

    return response


def error_log_timings(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t1 = datetime.now()
        result = func(*args, **kwargs)
        t2 = datetime.now()
        ctx.log.error(
            "%s finished in %.3f seconds", func.__name__, (t2 - t1).total_seconds()
        )
        return result

    return wrapper
