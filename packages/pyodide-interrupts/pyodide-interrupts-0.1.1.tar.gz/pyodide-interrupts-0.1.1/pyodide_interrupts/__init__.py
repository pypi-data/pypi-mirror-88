from . import _pyodide_interrupts
from contextlib import contextmanager

@contextmanager
def check_interrupts(callback, interval):
    """ Executes ``callback`` every ``interval`` many opcodes of Python bytecode. Uses tracing machinery. 
        We're going to use this to handle user interrupts.
    """
    _pyodide_interrupts.set_interval(interval)
    _pyodide_interrupts.start(callback)
    try:
        yield
    finally:
        _pyodide_interrupts.end()


# def check_interrupt(interrupt_buffer):
#     def helper():
#         if interrupt_buffer() == 0:
#             return
#         raise KeyboardInterrupt()
#     return helper
