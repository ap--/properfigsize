"""properfigsize module

If you are using pdflatex and matplotlib to embed plots in a PDF,
you can use this module to adjust your figure sizes correctly.

It's a two step process, where properfigsize runs pdflatex, to
aquire the final figure sizes in the PDF. These figure sizes are
then used to create the figures.
"""
import collections
import logging
import os.path
import re
import subprocess
import tempfile

# logging configuration
# =====================
logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")
_logger = logging.getLogger("properfigsize")


# module variables, classes and functions
# =======================================
RATIOLIMITS = (0.99, 1.01)
TEXFIGURESIZES = collections.OrderedDict()
SILENT = False


class Figsize(object):

    def __init__(self, name, ratio=4.0/3.0):
        self._name = str(name)
        self._ratio = float(ratio)

    def __iter__(self):
        return iter(self._get_proper_figsize_tuple())

    def _get_proper_figsize_tuple(self):
        global TEXFIGURESIZES
        try:
            fs = TEXFIGURESIZES[self._name]
            tex_ratio = fs[0]/fs[1]
            fig_ratio = self._ratio
            if RATIOLIMITS[0] < (tex_ratio / fig_ratio) < RATIOLIMITS[1]:
                _debug_print("'%s' proper size is %fin x %fin" %
                             (self._name, fs[0], fs[1]))
            else:
                _debug_print("'%s' ratio changed. Using default size." %
                             self._name)
                fs = (8.0, 8.0/self._ratio)
        except KeyError:
            fs = (8.0, 8.0/self._ratio)
            _debug_print("Could not find '%s' in tex." % self._name)
        return fs


def set_tex(texfile):
    """collects figure size information from pdflatex output.

    Args:
        texfile (str): File name of tex file.

    Returns:
        None
    """
    fs = _figure_sizes_from_pdflatex(texfile)
    TEXFIGURESIZES.update(fs)


# INTERNALS
# =========
def _debug_print(string):
    """module internal console output"""
    if not SILENT:
        _logger.info(string)


def _figure_sizes_from_pdflatex(texfile):
    """collects figure sizes from pdflatex output as dict."""
    data = _get_compile_log_from_pdflatex(texfile)
    _img = _parse_compile_log(data)

    figs = collections.OrderedDict()
    for i in range(len(_img)):
        figs[_img[i][0]] = _points_to_inch(*_img[i][1])

    return figs


def _get_compile_log_from_pdflatex(texfile):
    """returns log output from pdflatex call"""
    tempdir = tempfile.mkdtemp()

    try:
        subprocess.check_output(['pdflatex', '-draftmode', '-halt-on-error',
                                 '-output-directory=%s' % tempdir, texfile])
    except subprocess.CalledProcessError:
        _debug_print('pdflatex call failed. Ignore if first pass.')
        return None

    logfile = '%s.log' % texfile[:-4]
    fn = os.path.join(tempdir, logfile)
    with open(fn, 'r') as f:
        data = f.read()
    return data


def _parse_compile_log(log):
    """parses the pdflatex compile log"""
    if log is None:
        return {}

    IMAGES = {}
    i = 0
    image_found = False
    for line in log.split('\n'):
        if not image_found:
            m = re.match("^File: (.*) Graphic file", line)
            if m:
                IMAGES[i] = [m.group(1)]
                image_found = True
        else:
            ret = re.search("Requested size: (.*)\.", line)
            if ret is not None:
                IMAGES[i].append(ret.group(1).split(' x '))
                i += 1
                image_found = False

    return IMAGES


def _points_to_inch(*args):
    """module internal conversion function."""
    D = []
    for x in args:
        if x[-2:] != 'pt':
            raise ValueError("Length is not using point unit '%s'" % x)
        D.append(float(x[:-2])/72.27)
    return tuple(D)
