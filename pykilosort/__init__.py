import logging
import os

if os.getenv('MOCK_CUPY', False):
    from pykilosort.testing.mock_cupy import cupy 
    from pykilosort.testing.mock_cupyx import cupyx
else:
    import cupy
    import cupyx

from .utils import Bunch, memmap_binary_file, read_data, load_probe, plot_dissimilarity_matrices, plot_diagnostics
from .main import run, run_export, run_spikesort, run_preprocess
from .io.probes import np1_probe, np2_probe, np2_4shank_probe


__version__ = 'ibl_1.4.1'

# Set a null handler on the root logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


_logger_fmt = '%(asctime)s.%(msecs)03d [%(levelname)s] %(caller)s %(message)s'
_logger_date_fmt = '%H:%M:%S'


class _Formatter(logging.Formatter):
    def format(self, record):
        # Only keep the first character in the level name.
        record.levelname = record.levelname[0]
        filename = os.path.splitext(os.path.basename(record.pathname))[0]
        record.caller = '{:s}:{:d}'.format(filename, record.lineno).ljust(20)
        message = super(_Formatter, self).format(record)
        color_code = {'D': '90', 'I': '0', 'W': '33', 'E': '31'}.get(record.levelname, '7')
        message = '\33[%sm%s\33[0m' % (color_code, message)
        return message


def add_default_handler(level='INFO', logger=logger, filename=None):
    if filename is None:
        handler = logging.StreamHandler()
    else:
        handler = logging.FileHandler(filename)
    handler.setLevel(level)
    formatter = _Formatter(fmt=_logger_fmt, datefmt=_logger_date_fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
