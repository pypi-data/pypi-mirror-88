from kitchenart import _logger

try:
    import parler
    import parler_rest
except ModuleNotFoundError:
    _logger.exception('This module requires parler and parler_rest')
    raise
