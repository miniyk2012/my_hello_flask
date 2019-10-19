import os
import threading

from loguru import logger


def get_val(thread_local):
    try:
        return thread_local.val
    except AttributeError:
        return None


def register(app):
    thread_local = threading.local()

    @app.route('/set-threadlocal/<val>')
    def set_threadlocal(val):
        logger.info(threading.activeCount())
        thread_local.val = val
        logger.info('set val={}, thread_id={}, threadname={}, pid={}'
                    .format(get_val(thread_local), threading.currentThread().ident, threading.currentThread().name,
                            os.getpid()))
        return get_val(thread_local)

    @app.route('/get-threadlocal')
    def get_threadlocal():
        logger.info(threading.activeCount())
        logger.info('get val={}, thread_id={}, threadname={}, pid={}'
                    .format(get_val(thread_local), threading.currentThread().ident, threading.currentThread().name, os.getpid()))
        return get_val(thread_local) or 'failure'
