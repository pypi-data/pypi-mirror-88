"""
loggin utilities
"""
from contextlib import contextmanager
import logging
import time


def progressbar(iterable, log=None):
    """
    Args:
        iterable
        log (logger): optional

    Examples:
        >>> import logging
        >>> import rna
        >>> import sys
        >>> sys.modules['tqdm'] = None
        >>> log = logging.getLogger(__name__)

        >>> a = range(3)
        >>> for value in rna.log.progressbar(a, log=log):
        ...     _ = value * 3

    """
    if log is None:
        log = logging
    try:
        # tqdm not required for the module to work
        from tqdm import tqdm as progressor  # pylint: disable=import-outside-toplevel

        tqdm_exists = True
    except ImportError:

        def progressor(iterable):
            """
            dummy function. Does nothing
            """
            return iterable

        tqdm_exists = False
    try:
        n_total = len(iterable)
    except TypeError:
        n_total = None

    for i in progressor(iterable):
        if not tqdm_exists:
            if n_total is None:
                log.info("Progress: item {i}".format(**locals()))
            else:
                log.info("Progress: {i} / {n_total}".format(**locals()))
        yield i


@contextmanager
def timeit(process_name="No Description", log=None, precision=1) -> None:
    """
    Context manager for autmated timeing

    Args:
        process_name (str): message to customize the log message
        log (logger)
        precision (int): show until 10^-<precision> digits

    Examples:
        >>> import rna
        >>> with rna.log.timeit("Logger Name"):
        ...     # Some very long calculation
        ...     pass
    """
    if log is None:
        log = logging
    start_time = time.time()
    message = "Timing Process: {0} ...".format(process_name)
    log.log(logging.INFO, message)

    yield

    log.log(
        logging.INFO,
        "\t\t\t\t\t\t... Process Duration:"
        "{value:1.{precision}f} s".format(
            value=time.time() - start_time, precision=precision
        ),
    )
