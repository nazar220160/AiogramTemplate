from contextlib import suppress

with suppress(ImportError):
    import uvloop as _uvloop

    _uvloop.install()
