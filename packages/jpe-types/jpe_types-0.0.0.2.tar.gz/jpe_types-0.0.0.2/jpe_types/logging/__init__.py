"""logging

logging module add mainly utils for logThread and @log decorator to log function calles"""

from jpe_types.logging import logUtils
from jpe_types.logging.threadLogging import log, _setupLoggers

def setup(runName=None):
    """setup the loggers
    
    @param runName: overide to std run name if None default us std values set in loggingConfig.json
    @type runName: str or None"""
    assert isinstance(runName, str) or runName is None, f"runName must be str or None not {type(runName)}"
    setattr(logUtils, "runFile", logUtils.create_newRun(runName))

    _setupLoggers()