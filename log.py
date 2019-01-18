# -*-coding:utf-8-*-
import datetime
import logging
import logging.handlers
from logging import LogRecord
import os
import sys
import threading

from Src.conf.config import ROOT_DIR

logger_object = dict()

sensitive_Str = ['Password', 'PASSWORD', 'password', 'Pswd',
                 'PSWD', 'pwd', 'signature', 'HmacSHA256',
                 'private', 'certfile', 'secret', 'token', 'Token']


# 日志级别类
class LOGLEVEL(object):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    WARNING = logging.WARNING
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR


# 日志默认配置
class LOGCONFIG(object):
    DEFAULT_FORMATTER = "%(asctime)s %(name)s %(levelname)s [pid:%(process)d] [thread:%(thread)d %(threadName)s]" \
                        " [file:%(filename)s] [line:%(lineno)d] [func:%(funcName)s] %(message)s"
    DEFAULT_LEVEL = LOGLEVEL.INFO
    DEFAULT_LOG_PATH = ROOT_DIR


# 日志记录对象
GLOBAL_LOGGER = None


class Logger(object):
    def __init__(self, name_en, path):
        path = os.path.join(path, "{}.{}".format(name_en, "log"))
        logger = logging.getLogger(name_en)
        file_handler1 = logging.handlers.RotatingFileHandler(
            path, maxBytes=1024 * 1024 * 200, backupCount=50)
        logger.addHandler(file_handler1)
        logger.addFilter(DefaultLogFilter())
        logger.setLevel(logging.INFO)
        self.logger = logger
        self.file_handler = file_handler1

    def info(self, msg, threadname1, *args, **kwargs):
        try:
            raise Exception
        except Exception:
            f = sys.exc_info()[2].tb_frame.f_back.f_back
            co_name, lineno, file_name = f.f_code.co_name, f.f_lineno, f.f_code.co_filename
            file_name = file_name.rsplit('\\', 1)[-1]
        # 日志格式拼接
        msg = set_Formatter(threadname1, file_name, lineno, co_name, msg, "INFO")
        self.logger.info(msg, *args, **kwargs)

    def warn(self, msg, threadname1, *args, **kwargs):
        try:
            raise Exception
        except Exception:
            f = sys.exc_info()[2].tb_frame.f_back.f_back
            co_name, lineno, file_name = f.f_code.co_name, f.f_lineno, f.f_code.co_filename
            file_name = file_name.rsplit('\\', 1)[-1]
        # 日志格式拼接
        msg = set_Formatter(threadname1, file_name, lineno, co_name, msg, "WARN")
        self.logger.warn(msg, *args, **kwargs)

    def error(self, msg, threadname1, *args, **kwargs):
        try:
            raise Exception
        except Exception:
            f = sys.exc_info()[2].tb_frame.f_back.f_back
            co_name, lineno, file_name = f.f_code.co_name, f.f_lineno, f.f_code.co_filename
            file_name = file_name.rsplit('\\', 1)[-1]
        # 日志格式拼接
        msg = set_Formatter(threadname1, file_name, lineno, co_name, msg, "ERROR")
        self.logger.error(msg, *args, **kwargs)

    def debug(self, msg, threadname1, *args, **kwargs):
        try:
            raise Exception
        except Exception:
            f = sys.exc_info()[2].tb_frame.f_back.f_back
            co_name, lineno, file_name = f.f_code.co_name, f.f_lineno, f.f_code.co_filename
            file_name = file_name.rsplit('\\', 1)[-1]
        # 日志格式拼接
        msg = set_Formatter(threadname1, file_name, lineno, co_name, msg, "DEBUG")
        self.logger.debug(msg, *args, **kwargs)

    def critical(self, msg, threadname1, *args, **kwargs):
        try:
            raise Exception
        except Exception:
            f = sys.exc_info()[2].tb_frame.f_back.f_back
            co_name, lineno, file_name = f.f_code.co_name, f.f_lineno, f.f_code.co_filename
            file_name = file_name.rsplit('\\', 1)[-1]
        # 日志格式拼接
        msg = set_Formatter(threadname1, file_name, lineno, co_name, msg, "CRITICAL")
        self.logger.critical(msg, *args, **kwargs)

    def warning(self, msg, threadname1, *args, **kwargs):
        try:
            raise Exception
        except Exception:
            f = sys.exc_info()[2].tb_frame.f_back.f_back
            co_name, lineno, file_name = f.f_code.co_name, f.f_lineno, f.f_code.co_filename
            file_name = file_name.rsplit('\\', 1)[-1]
        # 日志格式拼接
        msg = set_Formatter(threadname1, file_name, lineno, co_name, msg, "WARNING")
        self.logger.warning(msg, *args, **kwargs)

    def close(self):
        self.file_handler.close()


def set_Formatter(threadname, file_name, lineno, co_name, msg, level):
    thread_id = threading.get_ident()
    thread_name = threading.current_thread().name
    for sen in sensitive_Str:
        if sen in thread_name:
            thread_name = thread_name.replace(sen, 'XXX')
    if hasattr(os, 'getpid'):
        process_id = os.getpid()
    else:
        process_id = None
    ct = datetime.datetime.now()
    current_time_in_microsecond = ct.strftime("%Y-%m-%d %H:%M:%S") + "," + str(ct.microsecond)[0:3]
    msg = "{} {} {} [pid:{}] [thread:{} {}] [file:{}] [line:{}] [func:{}] {}".format(
        str(current_time_in_microsecond), str(threadname), level, str(process_id),
        str(thread_id), str(thread_name), str(file_name), str(lineno), str(co_name), str(msg))
    return msg


def init(module_name=None):
    global GLOBAL_LOGGER
    # 日志对象已经初始化过
    if GLOBAL_LOGGER is not None:
        warn("log has been init.this init name is %s." % module_name)
        return
    # 未传入日志注册模块或者传入的对象为None，相关日志打印到default目录下
    if module_name is None:
        module_name = "default"

    # 检测日志父目录是否存在，不存在则创建
    if os.path.exists(LOGCONFIG.DEFAULT_LOG_PATH):
        if os.path.isfile(LOGCONFIG.DEFAULT_LOG_PATH):
            raise Exception("path %s is not directory." % LOGCONFIG.DEFAULT_LOG_PATH)
    else:
        os.makedirs(LOGCONFIG.DEFAULT_LOG_PATH)

    # 检测组件日志目录是否存在
    component_log_path = os.path.join(LOGCONFIG.DEFAULT_LOG_PATH, module_name)
    if os.path.exists(component_log_path):
        if os.path.isfile(component_log_path):
            raise Exception("path %s is not directory." % component_log_path)
    else:
        os.makedirs(component_log_path)

    log_file = os.path.join(component_log_path, module_name + ".log")

    # 初始化日志记录句柄
    log_file_handler = DefaultLogFileHandler(log_file)
    log_file_handler.setFormatter(logging.Formatter(LOGCONFIG.DEFAULT_FORMATTER))
    # 初始化日志对象
    GLOBAL_LOGGER = DefaultLogger(module_name)
    GLOBAL_LOGGER.addHandler(log_file_handler)
    GLOBAL_LOGGER.setLevel(LOGCONFIG.DEFAULT_LEVEL)
    GLOBAL_LOGGER.addFilter(DefaultLogFilter())

    # jilinyong test console 打印日志，正式发布的时候去掉
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s][%(name)s][%(levelname)s][%(process)d][%(thread)d][%(filename)s %(lineno)d][%(message)s]')
    console_handler.setFormatter(formatter)
    GLOBAL_LOGGER.addHandler(console_handler)

    # 设置日志文件权限
    os.chmod(log_file, 0o640)


def set_file_name(threadname):
    # 检测日志父目录是否存在，不存在则创建
    if os.path.exists(LOGCONFIG.DEFAULT_LOG_PATH):
        if os.path.isfile(LOGCONFIG.DEFAULT_LOG_PATH):
            raise Exception("path %s is not directory." % LOGCONFIG.DEFAULT_LOG_PATH)
    else:
        os.makedirs(LOGCONFIG.DEFAULT_LOG_PATH)
    # 检测组件日志目录是否存在
    component_log_path = os.path.join(LOGCONFIG.DEFAULT_LOG_PATH, threadname)
    if os.path.exists(component_log_path):
        if os.path.isfile(component_log_path):
            raise Exception("path %s is not directory." % component_log_path)
    else:
        os.makedirs(component_log_path)
    return component_log_path


def set_logger(threadname, component_log_path):
    if threadname not in logger_object.keys():
        loge = Logger("execute", component_log_path)
        logger_object[threadname] = loge


def debug(msg, *args, **kwargs):
    global GLOBAL_LOGGER
    if GLOBAL_LOGGER is None:
        raise Exception("not register log module.")
    GLOBAL_LOGGER.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    threadname = threading.current_thread().name
    Threadxx = threadname.isdigit()
    if not Threadxx:
        global GLOBAL_LOGGER
        if GLOBAL_LOGGER is None:
            raise Exception("not register log module.")
        GLOBAL_LOGGER.info(msg, *args, **kwargs)
    else:
        # 设置线程名与日志对象的关系
        component_log_path = set_file_name(threadname)
        set_logger(threadname, component_log_path)
        logger_object[threadname].info(msg, threadname, *args, **kwargs)
        logger_object[threadname].close()


def warning(msg, *args, **kwargs):
    threadname = threading.current_thread().name
    Threadxx = threadname.isdigit()
    if not Threadxx:
        global GLOBAL_LOGGER
        if GLOBAL_LOGGER is None:
            raise Exception("not register log module.")
        GLOBAL_LOGGER.warning(msg, *args, **kwargs)
    else:
        # 设置线程名与日志对象的关系
        component_log_path = set_file_name(threadname)
        set_logger(threadname, component_log_path)
        logger_object[threadname].warning(msg, threadname, *args, **kwargs)
        logger_object[threadname].close()


def warn(msg, *args, **kwargs):
    threadname = threading.current_thread().name
    Threadxx = threadname.isdigit()
    if not Threadxx:
        global GLOBAL_LOGGER
        if GLOBAL_LOGGER is None:
            raise Exception("not register log module.")
        GLOBAL_LOGGER.warn(msg, *args, **kwargs)
    else:
        # 设置线程名与日志对象的关系
        component_log_path = set_file_name(threadname)
        set_logger(threadname, component_log_path)
        logger_object[threadname].warn(msg, threadname, *args, **kwargs)
        logger_object[threadname].close()


def error(msg, *args, **kwargs):
    threadname = threading.current_thread().name
    Threadxx = threadname.isdigit()
    if not Threadxx:
        global GLOBAL_LOGGER
        if GLOBAL_LOGGER is None:
            raise Exception("not register log module.")
        GLOBAL_LOGGER.error(msg, *args, **kwargs)
    else:
        # 设置线程名与日志对象的关系
        component_log_path = set_file_name(threadname)
        set_logger(threadname, component_log_path)
        logger_object[threadname].error(msg, threadname, *args, **kwargs)
        logger_object[threadname].close()


def critical(msg, *args, **kwargs):
    threadname = threading.current_thread().name
    Threadxx = threadname.isdigit()
    if not Threadxx:
        global GLOBAL_LOGGER
        if GLOBAL_LOGGER is None:
            raise Exception("not register log module.")
        GLOBAL_LOGGER.critical(msg, *args, **kwargs)
    else:
        # 设置线程名与日志对象的关系
        component_log_path = set_file_name(threadname)
        set_logger(threadname, component_log_path)
        logger_object[threadname].critical(msg, threadname, *args, **kwargs)
        logger_object[threadname].close()


def setLevel(level):
    global GLOBAL_LOGGER
    if GLOBAL_LOGGER is None:
        raise Exception("not register log module.")
    GLOBAL_LOGGER.setLevel(level)


def addFilter(filter_handler):
    global GLOBAL_LOGGER
    if GLOBAL_LOGGER is None:
        raise Exception("not register log module.")
    GLOBAL_LOGGER.addFilter(filter=filter_handler)


class DefaultLogFilter(object):
    def filter(self, record):
        return self.__hasSensitiveStr(record.getMessage())

    @staticmethod
    def __hasSensitiveStr(inStr):
        sensitiveStr = ['Password', 'PASSWORD', 'password', 'Pswd',
                        'PSWD', 'pwd', 'signature', 'HmacSHA256',
                        'private', 'certfile', 'secret', 'token', 'Token']
        for item in sensitiveStr:
            if item in str(inStr):
                return False
        return True


class DefaultLogFileHandler(logging.handlers.WatchedFileHandler):
    def __init__(self, logfile, when="D", backupCount=0, encoding=None, delay=0):
        '''

        :param logfile: 日志文件（需要保证日志文件所在的路径是存在的）
        :param when: 日志转储的周期，默认是按天进行转储
        :param backupCount: 日志文件备份的数量，默认无限备份，即不删除任何备份的日志文件
        :param encoding:
        :param delay:
        '''
        self.file = logfile
        self.when = when.upper()

        if self.when == "D":
            # 以天为转储单位
            self.suffix = "%Y-%m-%d"
        elif self.when == "S":
            # 以秒为转储单位
            self.suffix = "%Y-%m-%d_%H-%M-%S"
        elif self.when == "M":
            # 以分钟为转储单位
            self.suffix = "%Y-%m-%d_%H-%M"
        elif self.when == "H":
            # 以小时为转储单位
            self.suffix = "%Y-%m-%d_%H"
        else:
            raise Exception("%s is unsupport rollback interval." % self.when)

        self.backCount = backupCount
        self.delay = delay
        self.encoding = encoding

        logging.handlers.WatchedFileHandler.__init__(
            self, self.file, mode='a', encoding=self.encoding,
            delay=self.delay)

    def __shouldDumpLogFile(self):
        '''判断日志文件是否需要按转储规则进行转储

        :return:
        '''
        if not os.path.isfile(self.file):
            return False

        create_log_datetime = datetime.datetime.fromtimestamp(os.path.getctime(self.file)).strftime(self.suffix)
        now_datetime = datetime.datetime.now().strftime(self.suffix)

        if create_log_datetime != now_datetime:
            return True
        return False

    def __dumpLogFile(self):
        '''日志文件转储

        :return:
        '''
        if self.stream is not None:
            self.stream.flush()
            self.stream.close()

        create_log_datetime = datetime.datetime.fromtimestamp(os.path.getctime(self.file)).strftime(self.suffix)
        file_list = self.file.split("\\")
        file_list[-1] = file_list[-1].split(".")[0] + create_log_datetime + ".log"
        file_list = "\\".join(file_list)
        if self.file != self.file:
            os.rename(self.file, file_list)

        if not self.delay:
            self.stream = self._open()

        if self.backCount > 0:
            self.__processBackupLog()

    def __processBackupLog(self):
        '''处理日志备份数量，保持在backCount内

        :return:
        '''
        # 日志备份存留上限处理
        pass

    def emit(self, record):
        '''Emit a record

        :param record: log msg
        :return:
        '''
        try:
            if self.__shouldDumpLogFile():
                self.__dumpLogFile()
            logging.handlers.WatchedFileHandler.emit(self, record)

            # 设置日志文件权限
            if oct(os.stat(self.file).st_mode)[-3:] != "640":
                os.chmod(self.file, 0o640)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


class DefaultLogger(logging.Logger):
    def __init__(self, name):
        logging.Logger.__init__(self, name)

    def findCaller(self, stack_info=False):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == logging._srcfile:
                f = f.f_back
                continue
            rv = (co.co_filename, f.f_lineno, co.co_name, None)
            break
        return rv

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        """
        A factory method which can be overridden in subclasses to create
        specialized LogRecords.
        """
        rv = LogRecord(name, level, fn, lno, msg, args, exc_info, func)
        if extra is not None:
            for key in extra:
                if (key in ["message", "asctime"]) or (key in rv.__dict__):
                    raise KeyError(
                        "Attempt to overwrite %r in LogRecord" %
                        key)
                rv.__dict__[key] = extra[key]

            if "type" not in extra:
                rv.__dict__["type"] = "run"
        else:
            rv.__dict__["type"] = "run"
        return rv


def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except Exception:
        return sys.exc_info()[2].tb_frame.f_back


if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(4)
