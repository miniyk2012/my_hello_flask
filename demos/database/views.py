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
        thread_local.val = val
        logger.info('set val={}, {}'.format(get_val(thread_local), threading.currentThread().name))
        return get_val(thread_local)

    @app.route('/get-threadlocal')
    def get_threadlocal():
        logger.info('get val={}, {}'.format(get_val(thread_local), threading.currentThread().name))
        return get_val(thread_local) or 'failure'
