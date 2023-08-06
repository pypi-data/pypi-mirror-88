import logging
from functools import wraps
import os


def run_logger(func):
    """This wrapper logs all runs of _run_tensorfree writing to a log file.
    This is useful for anyone that encounters the program failing, as you
    can see which file caused the problem.

    Parameters
    ----------
    func : function
        Designed for _run_tensorfree, but can be applied elsewhere

    Returns
    -------
    wrapper : function
        The calling function wrapped with a logger
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wraps logging feature around function"""
        root_dir = os.path.abspath(os.curdir)
        log_file = os.path.join(root_dir, "tensorfree.log")
        log_form = "[%(asctime)s] %(levelname)-8s %(message)s"
        logging.basicConfig(
            level=logging.INFO, format=log_form, filename=log_file, filemode="w+"
        )

        logger = logging.getLogger("wrap_logger")
        logger.info(f"{func.__name__} - {args}")

        return func(*args, **kwargs)

    return wrapper
