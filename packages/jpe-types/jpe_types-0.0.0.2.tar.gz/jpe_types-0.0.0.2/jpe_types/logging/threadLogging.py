"""log decorator

add the log decorator 
"""
from jpe_types.logging import logUtils
from threading import current_thread
import jpe_types.paralel.thread
import os, traceback
from inspect import getfullargspec


main_Logger = None
"std logger"

error_Logger = None
"error used to log errors"

def _setupLoggers():
    """subproces of setup

    dont call directly
    """
    global main_Logger, error_Logger
    main_Logger = logUtils.Create_defaultLogger(logType="mainLogger")
    error_Logger= logUtils.Create_defaultLogger(logType="ErrorLoger", name="ErrorLogger")




def log(log=None, logName=f"{__name__} log", useStdLog=True, loggErrors=True):
    """logging decorator
        
        log function cals

        if the function has a parameter log (must be kwarg) or kwargs the logger used by the decorator to
        log the function call for further logging
            
        @param logger: optional overide logger
        @param logName: the name of the logger when generated
        @param useDtdLog: bool if true will use std logger (main Logger)"""
    if log is None and not useStdLog: 
        log = logUtils.Create_defaultLogger(name=logName)
    def wrap(fun):
        def getMsg(args, kwargs):
            return f"ran function {fun.__name__} with args {args} and kwargs {kwargs}"
        def endExecLog(val):
            return f"function {fun.__name__} execution ended with return val {val}"

        def call(args, kwargs, funLogger):
            data = getfullargspec(fun)
            try:
                if "log" in data[0] or not data[2] is None:
                    val = fun(*args, **kwargs, log=funLogger)
                else:
                    val =fun(*args, **kwargs)
            except Exception as e:
                if loggErrors:
                    for subLoggerStr in logUtils.logging_data["logErors"]:
                        # check weather initiated
                        if eval(subLoggerStr) is None:
                            raise logUtils.LogSetupError()

                        if logUtils.logging_data[logUtils.logging_data["logTranslator"][subLoggerStr]]["trackBack"]:
                            eval(subLoggerStr).error(traceback.format_exc())
                        else:
                            eval(subLoggerStr).error(e)
                        for msg in logUtils.logging_data[logUtils.logging_data["logTranslator"][subLoggerStr]]["errorLogMessage"]:
                            eval(subLoggerStr).error(msg)
                raise e
            funLogger.info(endExecLog(val))
            return val
            
                    
        def thread_log_wraper(args, kwargs):
            logg = current_thread().threadLogger
            logg.info(getMsg(args, kwargs))

            return call(args, kwargs, logg)
        
        def log_wraperNoType(args, kwargs):
            if main_Logger is None:
                raise logUtils.LogSetupError
            
            main_Logger.info(getMsg(args, kwargs))
            return call(args, kwargs, main_Logger)
        

        def log_wraper(args, kwargs):
            log.info(getMsg(args, kwargs))
            return call(args, kwargs, log)
        
        def wraper(*args, **kwargs):

            thread = current_thread()

            if isinstance(thread, jpe_types.paralel.thread.LogThread):
                return thread_log_wraper(args, kwargs)

            elif useStdLog:
                return log_wraperNoType(args, kwargs)
            
            return log_wraper(args, kwargs)

        return wraper
    return wrap
