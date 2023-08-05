# -*- coding: utf-8 -*-
#
# This file is part of the pyFDA project hosted at https://github.com/chipmuenk/pyfda
#
# Copyright © pyFDA Project Contributors
# Licensed under the terms of the MIT License
# (see file LICENSE in root directory for details)

"""
Library with various general functions and variables needed by the pyfda routines
"""

import os, re, io
import sys, time
import struct
from contextlib import redirect_stdout
import logging
logger = logging.getLogger(__name__)
import numpy as np
from numpy import pi, log10, sin, cos
import numexpr
import markdown

import scipy.signal as sig

from distutils.version import LooseVersion
import pyfda.libs.pyfda_dirs as dirs

####### VERSIONS and related stuff ############################################
# ================ Required Modules ============================
# ==
# == When one of the following imports fails, terminate the program
V_NP = np.__version__
V_NUM = numexpr.__version__
from scipy import __version__ as V_SCI
from matplotlib import __version__ as V_MPL
from .compat import QT_VERSION_STR as V_QT
from .compat import PYQT_VERSION_STR as V_PYQT
from markdown import __version__ as V_MD

# redirect stdio output of show_config to string
f = io.StringIO()
with redirect_stdout(f):
    np.show_config()
INFO_NP = f.getvalue()

if 'mkl_info' in INFO_NP:
    MKL = " (mkl)"
else:
    MKL = ""

#logger.warning(INFO_NP)


__all__ = ['cmp_version', 'mod_version',
           'set_dict_defaults', 'clean_ascii', 'qstr', 'safe_eval',
           'dB', 'lin2unit', 'unit2lin',
           'cround', 'H_mag', 'cmplx_sort', 'unique_roots', 'impz',
           'expand_lim', 'format_ticks', 'fil_save', 'fil_convert', 'sos2zpk',
           'round_odd', 'round_even', 'ceil_odd', 'floor_odd','ceil_even', 'floor_even',
           'to_html', 'calc_Hcomplex']

PY32_64 = struct.calcsize("P") * 8 # yields 32 or 64, depending on 32 or 64 bit Python

V_PY = ".".join(map(str, sys.version_info[:3])) + " (" + str(PY32_64) + " Bit)"

# ================ Required Modules ============================
MODULES = {'python':       {'V_PY':V_PY},
           'matplotlib':   {'V_MPL':V_MPL},
           'Qt5':          {'V_QT':V_QT},
           'pyqt':         {'V_PYQT':V_PYQT},
           'numpy':        {'V_NP':V_NP},
           'numexpr':      {'V_NUM':V_NUM},
           'scipy':        {'V_SCI':V_SCI + MKL},
           'markdown':     {'V_MD':V_MD}
           }

# ================ Optional Modules ============================

try:
    from pyfixp import __version__ as V_FX
    MODULES.update({'pyfixp' : {'V_FX':V_FX}})
except ImportError:
    MODULES.update({'pyfixp': {'V_FX':None}})

try:
    import migen
    MODULES.update({'migen': {'V_MG':'installed'}})
except (ImportError,SyntaxError):
    MODULES.update({'migen':{'V_MG':None}})

try:
    from nmigen import __version__ as V_NMG
    MODULES.update({'nMigen': {'V_NMG':V_NMG}})
except ImportError:
    pass

try:
    from docutils import __version__ as V_DOC
    MODULES.update({'docutils': {'V_DOC':V_DOC}})
except ImportError:
    pass

try:
    from mplcursors import __version__ as V_CUR
    MODULES.update({'mplcursors': {'V_CUR':V_CUR}})
except ImportError:
    pass

try:
    from xlwt import __version__ as V_XLWT
    MODULES.update({'xlwt': {'V_XLWT':V_XLWT}})
except ImportError:
    pass

try:
    from xlsxwriter import __version__ as V_XLSX
    MODULES.update({'xlsx': {'V_XLSX':V_XLSX}})
except ImportError:
    pass

# Remove module names as keys and return a dict with items like
#  {'V_MPL':'3.3.1', ...}
MOD_VERSIONS = {}
for k in MODULES.keys():
    MOD_VERSIONS.update(MODULES[k])

CRLF = os.linesep # Windows: "\r\n", Mac OS: "\r", *nix: "\n"

def cmp_version(mod, version):
    """
    Compare version number of installed module `mod` against string `version` and
    return 1, 0 or -1 if the installed version is greater, equal or less than
    the number in `version`. If `mod` is not installed, return -2.

    Parameters
    ----------

    mod : str
        name of the module to be compared

    version : str
        version number in the form e.g. "0.1.6"

    Returns
    -------

    result : int
        one of the following error codes:

         :-2: module is not installed

         :-1: version of installed module is lower than the specified version

         :0: version of installed module is equal to specied version

         :1: version of installed module is higher than specified version

    """
    try:
        if mod not in MODULES or not MODULES[mod].values():
            return -2
        else:
            inst_ver = list(MODULES[mod].values())[0] # get dict value without knowing the key

        if LooseVersion(inst_ver) > LooseVersion(version):
            return 1
        elif  LooseVersion(inst_ver) == LooseVersion(version):
            return 0
        else:
            return -1
    except (TypeError, KeyError) as e:
        logger.warning("Version number of {0} could not be determined.\n"
                       "({1})".format(mod,e))
        return -1


def mod_version(mod = None):
    """
    Return the version of the module 'mod'. If the module is not found, return
    None. When no module is specified, return a string with all modules and
    their versions sorted alphabetically.
    """
    if mod:
        if mod in MODULES:
            return LooseVersion(list(MODULES[mod].values())[0])
        else:
            return None
    else:
        v_md = ""
        with open(os.path.join(dirs.INSTALL_DIR, "module_versions.md"), 'r') as f:
            # return a list, split at linebreaks while keeping linebreaks
            v = f.read().splitlines(True)

        for l in v:
            try:
                v_md += l.format(**MOD_VERSIONS) # evaluate {V_...} from MOD_VERSIONS entries
            except (KeyError) as e: # encountered undefined {V_...}
                logger.warning("KeyError: {0}".format(e)) # simply drop the line

        v_html = markdown.markdown(v_md, output_format='html5',
                                   extensions=['markdown.extensions.tables'])
        # pyinstaller needs explicit definition of extensions path

        return v_html

#------------------------------------------------------------------------------
logger.info(mod_version())

# Amplitude max, min values to prevent scipy aborts
# (Linear values)
MIN_PB_AMP  = 1e-5  # min pass band ripple
MAX_IPB_AMP = 0.85  # max pass band ripple IIR
MAX_FPB_AMP = 0.5  # max pass band ripple FIR
MIN_SB_AMP  = 1e-6  # max stop band attenuation
MAX_ISB_AMP = 0.65  # min stop band attenuation IIR
MAX_FSB_AMP = 0.45  # min stop band attenuation FIR

class ANSIcolors:
    """
    ANSI Codes for colors etc. in the console

    see https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
        https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    """
    if dirs.OS.lower() == "windows":
        os.system('color') # needed to activate colored terminal in Windows

    CEND      = '\33[0m'
    CBOLD     = '\33[1m'
    CFAINT    = '\33[2m'
    CITALIC   = '\33[3m'
    CURL      = '\33[4m' # underlined
    CBLINK    = '\33[5m' # slow blink
    CBLINK2   = '\33[6m' # fast blink
    CSELECTED = '\33[7m' # reverse video

    # Foreground colors
    BLACK  = '\33[30m'
    RED    = '\33[31m'
    GREEN  = '\33[32m'
    YELLOW = '\33[33m'
    BLUE   = '\33[34m'
    VIOLET = '\33[35m'
    CYAN   = '\33[36m'
    WHITE  = '\33[37m'

    # Background colors
    BLACKBG  = '\33[40m'
    REDBG    = '\33[41m'
    GREENBG  = '\33[42m'
    YELLOWBG = '\33[43m'
    BLUEBG   = '\33[44m'
    VIOLETBG = '\33[45m'
    CYANBG   = '\33[46m'
    WHITEBG  = '\33[47m'

    # Bright foreground colors
    GREY2   = '\33[90m'
    RED2    = '\33[91m'
    GREEN2  = '\33[92m'
    YELLOW2 = '\33[93m'
    BLUE2   = '\33[94m'
    VIOLET2 = '\33[95m'
    CYAN2   = '\33[96m'
    WHITE2  = '\33[97m'

    # Bright foreground colors
    GREYBG    = '\33[100m'
    REDBG2    = '\33[101m'
    GREENBG2  = '\33[102m'
    YELLOWBG2 = '\33[103m'
    BLUEBG2   = '\33[104m'
    VIOLETBG2 = '\33[105m'
    CYANBG2   = '\33[106m'
    WHITEBG2  = '\33[107m'


def clean_ascii(arg):
    """
    Remove non-ASCII-characters (outside range 0 ... x7F) from `arg` when it
    is a `str`. Otherwise, return `arg` unchanged.

    Parameters
    ----------
    arg: str
        This is a unicode string under Python 3 and a "normal" string under Python 2.

    Returns
    -------
    arg: str
         Input string, cleaned from non-ASCII characters

    """
    if isinstance(arg, str):
        return re.sub(r'[^\x00-\x7f]',r'', arg)
    else:
        return arg

#------------------------------------------------------------------------------
def qstr(text):
    """
    Convert text (QVariant, QString, string) or numeric object to plain string.

    In Python 3, python Qt objects are automatically converted to QVariant
    when stored as "data" (itemData) e.g. in a QComboBox and converted back when
    retrieving to QString.
    In Python 2, QVariant is returned when itemData is retrieved.
    This is first converted from the QVariant container format to a
    QString, next to a "normal" non-unicode string.

    Parameters
    ----------

    text: QVariant, QString, string or numeric data type that can be converted
      to string

    Returns
    -------

    The current `text` data as a unicode (utf8) string
    """
    return str(text)# tjos should be sufficient for Python 3 ?!

    text_type = str(type(text)).lower()

    if "qstring" in text_type:
        # Python 3: convert QString -> str
        #string = str(text)
        # Convert QString -> Utf8
        string = text.toUtf8()
    elif "qvariant" in text_type:
        # Python 2: convert QVariant -> QString
        string = text.toString()
        #string = QVariant(text).toString()
        #string = str(text.toString())
    elif "unicode" in text_type:
        return text
    else:
        # `text` is numeric or of type str
        string = str(text)

    return str(string) # convert QString -> str


###############################################################################
#### General functions ########################################################
###############################################################################

def np_type(a):
    """
    Return the python type of `a`, either of the parameter itself or (if it's a
    numpy array) of its items.

    Parameters
    ----------
    a : Python or numpy data type
        DESCRIPTION.

    Returns
    -------
    a_type : class
        Type of the Python variable resp. of the items of the numpy array

    """
    if isinstance(a, np.ndarray):
        a_type = type(a.item())
    else:
        a_type = type(a)

    return a_type

#-----------------------------------------------------------------------------

def set_dict_defaults(d, default_dict):
    """
    Add the key:value pairs of `default_dict` to dictionary `d` for all missing
    keys
    """
    if d is None or d == {}:
        d = default_dict
    else:
        for k,v in default_dict.items():
            if not k in d:
                d[k] = v

#------------------------------------------------------------------------------

def pprint_log(d, N=10, tab="\t"):
    """
    Provide pretty printed logging messages for dicts or lists.

    Convert dict `d` to string, inserting a CR+Tab after each key:value pair.

    If the value of dict key `d[k]` is a list or ndarray with more than `N` items,
    truncate it to `N` items.
    """
    s = tab
    #logger.info("Data: Type = {0}, ndim = {1}".format(type(d), np.ndim(d)))
    if type(d) == dict:
        for k in d:
            if type(d[k]) in {list, np.ndarray}:
                s += k + ' (L=' + str(len(d[k])) + ') :'\
                                + str(d[k][: min(N-1, len(d[k]))]) + ' ...'
            else:
                s += k + ' : ' + str(d[k])
            s += '\n' + tab
    elif type(d) in {list, np.ndarray}:
        #if type(d) == np.ndarray:
        #    d = d.tolist()
        if np.ndim(d) == 1:
            s += ('Type: {0} -> {1}, Shape =  ({2} x 1)\n' + tab).format(type(d), type(d[0]), len(d))
            s += str(d[: min(N-1, len(d))])
            if len(d) > N-1:
                s += ' ...'
        elif np.ndim(d) == 2:
            cols, rows = np.shape(d) #(outer, inner), inner (rows)is 1 or 2
            s += ('Type: {0} of {1}({2}), Shape = ({3} x {4})\n' + tab)\
                .format(type(d).__name__, type(d[0][0]).__name__, d[0][0].dtype, rows, cols)
                # use x.dtype.kind for general kind of numpy data
            logger.debug(s)
            for c in range(min(N-1, cols)):
                logger.debug('rows={0}; min(N-1, rows)={1}\nd={2}'\
                               .format(rows, min(N, rows), d[c][:min(N, rows)]))
                s += str(d[c][: min(N, rows)])
                if rows > N-1:
                    s += ' ...'+ '\n' + tab
                else:
                    s += '\n' + tab
    else:
        s = d

    return s

#------------------------------------------------------------------------------
def safe_numexpr_eval(expr, fallback=None, local_dict={}):
    """
    Evaluate `numexpr.evaluate(expr)` and catch various errors.

    Parameters
    ----------
    expr : str
        String to be evaluated and converted to a numpy array
    fallback : array-like or tuple
        numpy array or scalar as a fallback when errors occur during evaluation,
        this also defines the expected shape of the returned numpy expression

        When fallback is a tuple (e.g. '(11,)'), provide an array of zeros with the passed shape.
    local_dict : dict
        dict with variables passed to `numexpr.evaluate`

    Returns
    -------
    np_expr : array-like
        `expr` converted to a numpy array or scalar

    """
    if type(fallback) == tuple:
        np_expr = np.zeros(fallback) # fallback defines the shape
        fallback_shape = fallback
    else:
        np_expr = fallback # fallback is the default numpy return value or None
        fallback_shape = np.shape(fallback)

    try:
        np_expr = numexpr.evaluate(expr.strip(), local_dict=local_dict)
    except SyntaxError as e:
        logger.warning("Syntax error:\n\t{0}".format(e))
    except KeyError as e:
        logger.warning("Unknown variable {0}".format(e))
    except TypeError as e:
        logger.warning("Type error\n\t{0}".format(e))
    except AttributeError as e:
        logger.warning("Attribute error:\n\t{0}".format(e))
    except ValueError as e:
        logger.warning("Value error:\n\t{0}".format(e))
    except ZeroDivisionError:
        logger.warning("Zero division error in formula.")

    if np_expr is None:
        return None # no fallback, no error checking!
    # check if dimensions of converted string agree with expected dimensions
    elif np.ndim(np_expr) != np.ndim(fallback):
        if np.ndim(np_expr) == 0:
        # np_expr is scalar, return array with shape of fallback of constant values
            np_expr = np.ones(fallback_shape) * np_expr
        else:
        # return array of zeros in the shape of the fallback
            logger.warning("Expression has unexpected dimension {0}!".format(np.ndim(np_expr)))
            np_expr = np.zeros(fallback_shape)

    if np.shape(np_expr) != fallback_shape:
            logger.warning("Expression has unsuitable length {0}!".format(np.shape(np_expr)[0]))
            np_expr = np.zeros(fallback_shape)
    if not type(np_expr.item(0)) in {float, complex}:
        np_expr = np_expr.astype(float)

    return np_expr


def safe_eval(expr, alt_expr=0, return_type="float", sign=None):
    """
    Try ... except wrapper around numexpr to catch various errors
    When evaluation fails or returns `None`, try evaluating `alt_expr`. When this also fails,
    return 0 to avoid errors further downstream.

    Parameters
    ----------
    expr: str or scalar
       Expression to be evaluated, is cast to a string

    alt_expr: str or scalar
        Expression to be evaluated when evaluation of first string fails, is
        cast to a string.

    return_type: str
        Type of returned variable ['float' (default) / 'cmplx' / 'int' / '' or 'auto']

    sign: str
        enforce positive / negative sign of result ['pos', 'poszero' / None (default)
                                                    'negzero' / 'neg']

    Returns
    -------
    the evaluated result or 0 when both arguments fail: float (default) / complex / int


    Function attribute `err` contains number of errors that have occurred during
    evaluation (0 / 1 / 2)
    """
    # convert to str (PY3) resp. unicode (PY2) and remove non-ascii characters
    expr = clean_ascii(qstr(expr))
    alt_expr = clean_ascii(qstr(alt_expr))

    result = None
    fallback = ""
    safe_eval.err = 0 # initialize function attribute

    for ex in [expr, alt_expr]:
        if ex == "":
            result = None
            logger.error("Empty string passed to safe_eval!")
        else:
            if not return_type in {'float', 'int', 'cmplx', 'auto', ''}:
                logger.error('Unknown return type "{0}", setting result to 0.'.format(return_type))

            ex_num = safe_numexpr_eval(ex)
            if ex_num is not None:

                if return_type == 'cmplx':
                    result = ex_num.item()
                elif return_type == '' or return_type =='auto':
                    result = np.real_if_close(ex_num).item()
                else: # return_type == 'float' or 'int'
                    result = ex_num.real.item()

                if sign in {'pos', 'poszero'}:
                    result = np.abs(result)
                elif sign in {'neg', 'negzero'}:
                    result = -np.abs(result)

                if result == 0 and sign in {'pos', 'neg'}:
                    logger.warning(fallback + 'Argument must not be zero.')
                    result = None

                if return_type == 'int' and result is not None:
                    result = int(result.real) # convert to standard int type, not np.int64

        if result is not None:
            break # break out of for loop when evaluation has succeeded
        fallback = "Fallback: "
        safe_eval.err += 1

    if result is None:
        result = 0
    return result

#------------------------------------------------------------------------------
def to_html(text, frmt=None):
    """
    Convert text to HTML format:
        - pretty-print logger messages
        - convert "\\n" to "<br />
        - convert "< " and "> " to "&lt;" and "&gt;"
        - format strings with italic and / or bold HTML tags, depending on
          parameter `frmt`. When `frmt=None`, put the returned string between
          <span> tags to enforce HTML rendering downstream
        - replace '_' by HTML subscript tags. Numbers 0 ... 9 are never set to
          italic format

    Parameters
    ----------

    text: string
        Text to be converted

    frmt: string
        define text style

        - 'b' : bold text
        - 'i' : italic text
        - 'bi' or 'ib' : bold and italic text

    Returns
    -------

    string
        HTML - formatted text

    Examples
    --------

        >>> to_html("F_SB", frmt='bi')
        "<b><i>F<sub>SB</sub></i></b>"
        >>> to_html("F_1", frmt='i')
        "<i>F</i><sub>1</sub>"
    """
    # see https://danielfett.de/de/tutorials/tutorial-regulare-ausdrucke/
    # arguments for regex replacement with illegal characters
    # [a-dA-D] list of characters
    # \w : meta character for [a-zA-Z0-9_]
    # \s : meta character for all sorts of whitespace
    # [123][abc] test for e.g. '2c'
    # '^' means "not", '|' means "or" and '\' escapes, '.' means any character,
    # '+' means once or more, '?' means zero or once, '*' means zero or more
    #   '[^a]' means except for 'a'
    # () defines a group that can be referenced by \1, \2, ...
    #
    # '([^)]+)' : match '(', gobble up all characters except ')' till ')'
    # '(' must be escaped as '\('

    # mappings text -> HTML formatted logging messages

    if frmt == 'log':
        # only in logging messages replace e.g. in <class> the angled brackets
        # by HTML code
        mapping = [ ('<','&lt;'), ('>','&gt;')]
        for k,v in mapping:
            text = text.replace(k,v)

    mapping = [ ('< ','&lt;'), ('> ','&gt;'), ('\n','<br />'),
                ('\t','&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'),
                ('[  DEBUG]','<b>[  DEBUG]</b>'),
                ('[   INFO]','<b style="color:darkgreen;">[   INFO]</b>'),
                ('[WARNING]','<b style="color:orange;">[WARNING]</b>'),
                ('[  ERROR]','<b style="color:red">[  ERROR]</b>')
              ]

    for k, v in mapping:
         text = text.replace(k, v)
    html = text
    if frmt in {'i', 'bi', 'ib'}:
        html = "<i>" + html + "</i>"
    if frmt in {'b', 'bi', 'ib'}:
        html = "<b>" + html + "</b>"
    if frmt == None:
        html = "<span>" + html + "</span>"

    if frmt != 'log': # this is a label, not a logger message
        # replace _xxx (terminated by whitespace) by <sub> xxx </sub> ()
        html = re.sub(r'([<>a-zA-Z;])_(\w+)', r'\1<sub>\2</sub>', html)
        # don't render numbers as italic
#        if "<i>" in html:
#            html = re.sub(r'([<>a-zA-Z;_])([0-9]+)', r'\1<span class="font-style:normal">\2</span>', html)

    #(^|\s+)(\w{1})_(\w*)  # check for line start or one or more whitespaces
    # Replace group using $1$2<sub>$3</sub> (Py RegEx: \1\2<sub>\3</sub>)

    return html

###############################################################################
####     Scipy-like    ########################################################
###############################################################################

def dB(lin, power = False):
    """
    Calculate dB from linear value. If power = True, calculate 10 log ...,
    else calculate 20 log ...
    """
    if power:
        return 10. * np.log10(lin)
    else:
        return 20 * np.log10(lin)

def lin2unit(lin_value, filt_type, amp_label, unit = 'dB'):
    """
    Convert linear amplitude specification to dB or W, depending on filter
    type ('FIR' or 'IIR') and whether the specifications belong to passband
    or stopband. This is determined by checking whether amp_label contains
    the strings 'PB' or 'SB' :

    - Passband:
        .. math::

            \\text{IIR:}\quad A_{dB} &= -20 \log_{10}(1 - lin\_value)

            \\text{FIR:}\quad A_{dB} &=  20 \log_{10}\\frac{1 + lin\_value}{1 - lin\_value}

    - Stopband:
        .. math::

            A_{dB} = -20 \log_{10}(lin\_value)

    Returns the result as a float.
    """
    if unit == 'dB':
        if "PB" in amp_label: # passband
            if filt_type == 'IIR':
                unit_value = -20 * log10(1. - lin_value)
            else:
                unit_value = 20 * log10((1. + lin_value)/(1 - lin_value))
        else: # stopband
            unit_value = -20 * log10(lin_value)
    elif unit == 'W':
        unit_value = lin_value * lin_value
    else:
        unit_value = lin_value

    return unit_value


def unit2lin(unit_value, filt_type, amp_label, unit = 'dB'):
    """
    Convert amplitude specification in dB or W to linear specs:

    - Passband:
        .. math::

            \\text{IIR:}\quad A_{PB,lin} &= 1 - 10 ^{-unit\_value/20}

            \\text{FIR:}\quad A_{PB,lin} &= \\frac{10 ^ {unit\_value/20} - 1}{10 ^ {unit\_value/20} + 1}

    - Stopband:
        .. math::
            A_{SB,lin} = -10 ^ {-unit\_value/20}

    Returns the result as a float.
    """
    msg = "" # string for error message
    if np.iscomplex(unit_value) or unit_value < 0:
        unit_value = abs(unit_value)
        msg = "negative or complex, "

    if unit == 'dB':
        try:
            if "PB" in amp_label: # passband
                if filt_type == 'IIR':
                    lin_value = 1. - 10.**(-unit_value / 20.)
                else:
                    lin_value = (10.**(unit_value / 20.) - 1) / (10.**(unit_value / 20.) + 1)
            else: # stopband
                lin_value = 10.**(-unit_value / 20)

        except OverflowError:
            msg += "way "
            lin_value = 10 # definitely too large, will be limited in next section

    elif unit == 'W':
        lin_value = np.sqrt(unit_value)
    else:
        lin_value = unit_value

    # check limits to avoid errors during filter design
    if "PB" in amp_label: # passband
        if lin_value < MIN_PB_AMP:
            lin_value = MIN_PB_AMP
            msg += "too small, "
        if filt_type == 'IIR':
            if lin_value > MAX_IPB_AMP:
                lin_value = MAX_IPB_AMP
                msg += "too large, "
        elif filt_type == 'FIR':
            if lin_value > MAX_FPB_AMP:
                lin_value = MAX_FPB_AMP
                msg += "too large, "

    else: # stopband
        if lin_value < MIN_SB_AMP:
            lin_value = MIN_SB_AMP
            msg += "too small, "
        if filt_type == 'IIR':
            if lin_value > MAX_ISB_AMP:
                lin_value = MAX_ISB_AMP
                msg += "too large, "
        elif filt_type == 'FIR':
            if lin_value > MAX_FSB_AMP:
                lin_value = MAX_FSB_AMP
                msg += "too large, "

    if msg:
        logger.warning("Amplitude spec for {0} is ".format(amp_label) + msg + "using {0:.4g} {1} instead."\
                       .format(lin2unit(lin_value, filt_type=filt_type, amp_label=amp_label,unit=unit),
                               unit))

    return lin_value


def cround(x, n_dig = 0):
    """
    Round complex number to n_dig digits. If n_dig == 0, don't round at all,
    just convert complex numbers with an imaginary part very close to zero to
    real.
    """
    x = np.real_if_close(x, 1e-15)
    if n_dig > 0:
        if np.iscomplex(x):
            x = np.complex(np.around(x.real, n_dig), np.around(x.imag, n_dig))
        else:
            x = np.around(x, n_dig)
    return x

#------------------------------------------------------------------------------
    """
    Bandlimited periodic functions written by Endolith,
    https://gist.github.com/endolith/407991
    """

def sawtooth_bl(t):
    """
    Bandlimited sawtooth function as a direct replacement for
    `scipy.signal.sawtooth`. It is calculated by Fourier synthesis, i.e.
    by summing up all sine wave components up to the Nyquist frequency.
    """
    if t.dtype.char in ['fFdD']:
        ytype = t.dtype.char
    else:
        ytype = 'd'
    y = np.zeros(t.shape, ytype)
    # Get sampling frequency from timebase
    fs =  1 / (t[1] - t[0])
    # Sum all multiple sine waves up to the Nyquist frequency:
    for h in range(1, int(fs*pi)+1):
        y += 2 / pi * -sin(h * t) / h
    return y

def triang_bl(t):
    """
    Bandlimited triangle function as a direct replacement for
    `scipy.signal.sawtooth(width=0.5)`. It is calculated by Fourier synthesis, i.e.
    by summing up all sine wave components up to the Nyquist frequency.
    """
    if t.dtype.char in ['fFdD']:
        ytype = t.dtype.char
    else:
        ytype = 'd'
    y = np.zeros(t.shape, ytype)
    # Get sampling frequency from timebase
    fs =  1 / (t[1] - t[0])
    # Sum all multiple sine waves up to the Nyquist frequency:
    for h in range(1, int(fs * pi) + 1, 2):
        y += 8 / pi**2 * -cos(h * t) / h**2
    return y

def rect_bl(t, duty=0.5):
    """
    Bandlimited rectangular function as a direct replacement for
    `scipy.signal.square`. It is calculated by Fourier synthesis, i.e.
    by summing up all sine wave components up to the Nyquist frequency.
    """
    if t.dtype.char in ['fFdD']:
        ytype = t.dtype.char
    else:
        ytype = 'd'
    y = np.zeros(t.shape, ytype)
    # Get sampling frequency from timebase
    # Sum all multiple sine waves up to the Nyquist frequency:
    y = sawtooth_bl(t - duty*2*pi) - sawtooth_bl(t) + 2*duty-1
    return y

def comb_bl(t):
    """
    Bandlimited comb function. It is calculated by Fourier synthesis, i.e.
    by summing up all cosine components up to the Nyquist frequency.
    """
    if t.dtype.char in ['fFdD']:
        ytype = t.dtype.char
    else:
        ytype = 'd'
    y = np.zeros(t.shape, ytype)
    # Get sampling frequency from timebase
    # Sum all multiple sine waves up to the Nyquist frequency:
    fs =  1 / (t[1] - t[0])
    N = int(fs * pi) + 1
    for h in range(1, N):
        y += cos(h * t)
    y /= N
    return y
#------------------------------------------------------------------------------

def H_mag(num, den, z, H_max, H_min = None, log = False, div_by_0 = 'ignore'):
    """
    Calculate `\|H(z)\|` at the complex frequency(ies) `z` (scalar or
    array-like).  The function `H(z)` is given in polynomial form with numerator and
    denominator. When ``log == True``, :math:`20 \log_{10} (|H(z)|)` is returned.

    The result is clipped at H_min, H_max; clipping can be disabled by passing
    None as the argument.

    Parameters
    ----------
    num : float or array-like
        The numerator polynome of H(z).
    den : float or array-like
        The denominator polynome of H(z).
    z : float or array-like
        The complex frequency(ies) where `H(z)` is to be evaluated
    H_max : float
        The maximum value to which the result is clipped
    H_min : float, optional
        The minimum value to which the result is clipped (default: 0)
    log : boolean, optional
        When true, return 20 * log10 (\|H(z)\|). The clipping limits have to
        be given as dB in this case.
    div_by_0 : string, optional
        What to do when division by zero occurs during calculation (default:
        'ignore'). As the denomintor of H(z) becomes 0 at each pole, warnings
        are suppressed by default. This parameter is passed to numpy.seterr(),
        hence other valid options are 'warn', 'raise' and 'print'.

    Returns
    -------
    H_mag : float or ndarray
        The magnitude `\|H(z)\|` for each value of `z`.
    """

    try: len(num)
    except TypeError:
        num_val = abs(num) # numerator is a scalar
    else:
        num_val = abs(np.polyval(num, z)) # evaluate numerator at z
    try: len(den)
    except TypeError:
        den_val = abs(den) # denominator is a scalar
    else:
        den_val = abs(np.polyval(den, z)) # evaluate denominator at z

    olderr = np.geterr()  # store current floating point error behaviour
    # turn off divide by zero warnings, just return 'inf':
    np.seterr(divide = 'ignore')

    H_val = np.nan_to_num(num_val / den_val) # remove nan and inf
    if log:
        H_val = 20 * np.log10(H_val)


    np.seterr(**olderr) # restore previous floating point error behaviour

    # clip result to H_min / H_max
    return np.clip(H_val, H_min, H_max)

#----------------------------------------------
# from scipy.sig.signaltools.py:
def cmplx_sort(p):
    "sort roots based on magnitude."
    p = np.asarray(p)
    if np.iscomplexobj(p):
        indx = np.argsort(abs(p))
    else:
        indx = np.argsort(p)
    return np.take(p, indx, 0), indx

# adapted from scipy.signal.signaltools.py:
# TODO:  comparison of real values has several problems (5 * tol ???)
# TODO: speed improvements
def unique_roots(p, tol=1e-3, magsort = False, rtype='min', rdist='euclidian'):
    """
    Determine unique roots and their multiplicities from a list of roots.

    Parameters
    ----------
    p : array_like
        The list of roots.
    tol : float, default tol = 1e-3
        The tolerance for two roots to be considered equal. Default is 1e-3.
    magsort: Boolean, default = False
        When magsort = True, use the root magnitude as a sorting criterium (as in
        the version used in numpy < 1.8.2). This yields false results for roots
        with similar magniudes (e.g. on the unit circle) but is signficantly
        faster for a large number of roots (factor 20 for 500 double roots.)
    rtype : {'max', 'min, 'avg'}, optional
        How to determine the returned root if multiple roots are within
        `tol` of each other.
        - 'max' or 'maximum': pick the maximum of those roots (magnitude ?).
        - 'min' or 'minimum': pick the minimum of those roots (magnitude?).
        - 'avg' or 'mean' : take the average of those roots.
        - 'median' : take the median of those roots
    dist : {'manhattan', 'euclid'}, optional
        How to measure the distance between roots: 'euclid' is the euclidian
        distance. 'manhattan' is less common, giving the
        sum of the differences of real and imaginary parts.

    Returns
    -------
    pout : list
        The list of unique roots, sorted from low to high (only for real roots).
    mult : list
        The multiplicity of each root.

    Notes
    -----
    This utility function is not specific to roots but can be used for any
    sequence of values for which uniqueness and multiplicity has to be
    determined. For a more general routine, see `numpy.unique`.

    Examples
    --------
    >>> vals = [0, 1.3, 1.31, 2.8, 1.25, 2.2, 10.3]
    >>> uniq, mult = unique_roots(vals, tol=2e-2, rtype='avg')

    Check which roots have multiplicity larger than 1:

    >>> uniq[mult > 1]
    array([ 1.305])

    Find multiples of complex roots on the unit circle:
    >>> vals = np.roots(1,2,3,2,1)
    uniq, mult = unique_roots(vals, rtype='avg')

    """

    def manhattan(a,b):
        """
        Manhattan distance between a and b
        """
        return np.abs(a.real - b.real) + np.abs(a.imag - b.imag)

    def euclid(a,b):
        """
        Euclidian distance between a and b
        """
        return np.abs(a - b)

    if rtype in ['max', 'maximum']:
        comproot = np.max
    elif rtype in ['min', 'minimum']:
        comproot = np.min
    elif rtype in ['avg', 'mean']:
        comproot = np.mean
    elif rtype == 'median':
        comproot = np.median
    else:
        raise TypeError(rtype)

    if rdist in ['euclid', 'euclidian']:
        dist_roots = euclid
    elif rdist in ['rect', 'manhattan']:
        dist_roots = manhattan
    else:
        raise TypeError(rdist)

    mult = [] # initialize list for multiplicities
    pout = [] # initialize list for reduced output list of roots

    tol = abs(tol)
    p = np.atleast_1d(p) # convert p to at least 1D array
    if len(p) == 0:
        return pout, mult

    elif len(p) == 1:
        pout = p
        mult = [1]
        return pout, mult

    else:
        pout = p[np.isnan(p)].tolist() # copy nan elements to pout, convert to list
        mult = len(pout) * [1] # generate an (empty) list with a "1" for each nan
        p = p[~np.isnan(p)]    # delete nan elements from p, convert to list

        if len(p) == 0:
            pass

        elif (np.iscomplexobj(p) and not magsort):
            while len(p):
                # calculate distance of first root against all others and itself
                # -> multiplicity is at least 1, first root is always deleted
                tolarr = np.less(dist_roots(p[0], p), tol)                               # assure multiplicity is at least one
                mult.append(np.sum(tolarr)) # multiplicity = number of "hits"
                pout.append(comproot(p[tolarr])) # pick the roots within the tolerance

                p = p[~tolarr]  # and delete them

        else:
            sameroots = [] # temporary list for roots within the tolerance
            p,indx = cmplx_sort(p)
            indx = len(mult)-1
            curp = p[0] + 5 * tol # needed to avoid "self-detection" ?
            for k in range(len(p)):
                tr = p[k]
                if abs(tr - curp) < tol:
                    sameroots.append(tr)
                    curp = comproot(sameroots)  # not correct for 'avg'
                                                # of multiple (N > 2) root !
                    pout[indx] = curp
                    mult[indx] += 1
                else:
                    pout.append(tr)
                    curp = tr
                    sameroots = [tr]
                    indx += 1
                    mult.append(1)

        return np.array(pout), np.array(mult)

##### original code ####
#    p = asarray(p) * 1.0
#    tol = abs(tol)
#    p, indx = cmplx_sort(p)
#    pout = []
#    mult = []
#    indx = -1
#    curp = p[0] + 5 * tol
#    sameroots = []
#    for k in range(len(p)):
#        tr = p[k]
#        if abs(tr - curp) < tol:
#            sameroots.append(tr)
#            curp = comproot(sameroots)
#            pout[indx] = curp
#            mult[indx] += 1
#        else:
#            pout.append(tr)
#            curp = tr
#            sameroots = [tr]
#            indx += 1
#            mult.append(1)
#    return array(pout), array(mult)

#==================================================================
def calc_ssb_spectrum(A):
    """
    Calculate the single-sideband spectrum from a double-sideband
    spectrum by doubling the spectrum below fS/2 (leaving the DC-value
    untouched). This approach is wrong when the spectrum is not symmetric.
    
    The alternative approach of  adding the mirrored conjugate complex of the
    second half of the spectrum to the first doesn't work, spectra of either 
    sine-like or cosine-like signals are cancelled out.

    When len(A) is even, A[N//2] represents half the sampling frequencvy
    and is discarded (Q: also for the power calculation?).

    Parameters
    ----------
    A : array-like
        double-sided spectrum, usually complex. The sequence is as follows:

            [0, 1, 2, ..., 4, -5, -4, ... , -1] for len(A) = 10

    Returns
    -------
    A_SSB : array-like
        single-sided spectrum with half the number of input values

    """
    N = len(A)
    
    A_SSB = np.insert(A[1:N//2] * 2, 0, A[0])
    # A_SSB = np.insert(A[1:N//2] + A[-1:-(N//2):-1].conj(),0, A[0]) # doesn't work

    return A_SSB

#==================================================================
def impz(b, a=1, FS=1, N=0, step = False):
    """
Calculate impulse response of a discrete time filter, specified by
numerator coefficients b and denominator coefficients a of the system
function H(z).

When only b is given, the impulse response of the transversal (FIR)
filter specified by b is calculated.

Parameters
----------
b :  array_like
     Numerator coefficients (transversal part of filter)

a :  array_like (optional, default = 1 for FIR-filter)
     Denominator coefficients (recursive part of filter)

FS : float (optional, default: FS = 1)
     Sampling frequency.

N :  float (optional)
     Number of calculated points.
     Default: N = len(b) for FIR filters, N = 100 for IIR filters

Returns
-------
hn : ndarray with length N (see above)
td : ndarray containing the time steps with same


Examples
--------
>>> b = [1,2,3] # Coefficients of H(z) = 1 + 2 z^2 + 3 z^3
>>> h, n = dsp_lib.impz(b)
"""
    a = np.asarray(a)
    b = np.asarray(b)

    if len(a) == 1:
        if len(b) == 1:
            raise TypeError(
            'No proper filter coefficients: len(a) = len(b) = 1 !')
        else:
            IIR = False
    else:
        if len(b) == 1:
            IIR = True
        # Test whether all elements except first are zero
        elif not np.any(a[1:]) and a[0] != 0:
            #  same as:   elif np.all(a[1:] == 0) and a[0] <> 0:
            IIR = False
        else:
            IIR = True

    if N == 0: # set number of data points automatically
        if IIR:
            N = 100 # TODO: IIR: more intelligent algorithm needed
        else:
            N = min(len(b),  100) # FIR: N = number of coefficients (max. 100)

    impulse = np.zeros(N)
    impulse[0] =1.0 # create dirac impulse as input signal
    hn = np.array(sig.lfilter(b, a, impulse)) # calculate impulse response
    td = np.arange(len(hn)) / FS

    if step: # calculate step response
        hn = np.cumsum(hn)

    return hn, td

#==================================================================
def group_delay(b, a=1, nfft=512, whole=False, analog=False, verbose=True, fs=2.*pi, use_scipy = True):
#==================================================================
    """
Calculate group delay of a discrete time filter, specified by
numerator coefficients `b` and denominator coefficients `a` of the system
function `H` ( `z`).

When only `b` is given, the group delay of the transversal (FIR)
filter specified by `b` is calculated.

Parameters
----------
b :  array_like
     Numerator coefficients (transversal part of filter)

a :  array_like (optional, default = 1 for FIR-filter)
     Denominator coefficients (recursive part of filter)

whole : boolean (optional, default : False)
     Only when True calculate group delay around
     the complete unit circle (0 ... 2 pi)

verbose : boolean (optional, default : True)
    Print warnings about frequency point with undefined group delay (amplitude = 0)

nfft :  integer (optional, default: 512)
     Number of FFT-points

fs : float (optional, default: fs = 2*pi)
     Sampling frequency.


Returns
-------
tau_g : ndarray (the group delay)
w : ndarray, angular frequency points where group delay was computed

Notes
-----
The group delay :math:`\\tau_g(\\omega)` of discrete and continuous time
systems is defined by

.. math::

    \\tau_g(\\omega) = -  \\phi'(\\omega)
        = -\\frac{\\partial \\phi(\\omega)}{\\partial \\omega}
        = -\\frac{\\partial }{\\partial \\omega}\\angle H( \\omega)

A useful form for calculating the group delay is obtained by deriving the
*logarithmic* frequency response in polar form as described in [JOS]_ , [Lyons]_ for
discrete time systems:

.. math::

    \\ln ( H( \\omega))
      = \\ln \\left({H_A( \\omega)} e^{j \\phi(\\omega)} \\right)
      = \\ln \\left({H_A( \\omega)} \\right) + j \\phi(\\omega)

      \\Rightarrow \\; \\frac{\\partial }{\\partial \\omega} \\ln ( H( \\omega))
      = \\frac{H_A'( \\omega)}{H_A( \\omega)} +  j \\phi'(\\omega)

where :math:`H_A(\\omega)` is the amplitude response. :math:`H_A(\\omega)` and
its derivative :math:`H_A'(\\omega)` are real-valued, therefore, the group
delay can be calculated from

.. math::

      \\tau_g(\\omega) = -\\phi'(\\omega) =
      -\\Im \\left\\{ \\frac{\\partial }{\\partial \\omega}
      \\ln ( H( \\omega)) \\right\\}
      =-\\Im \\left\\{ \\frac{H'(\\omega)}{H(\\omega)} \\right\\}

The derivative of a polynome :math:`P(s)` (continuous-time system) or :math:`P(z)`
(discrete-time system) w.r.t. :math:`\\omega` is calculated by:

.. math::

    \\frac{\\partial }{\\partial \\omega} P(s = j \\omega)
    = \\frac{\\partial }{\\partial \\omega} \\sum_{k = 0}^N c_k (j \\omega)^k
    =  j \\sum_{k = 0}^{N-1} (k+1) c_{k+1} (j \\omega)^{k}
    =  j P_R(s = j \\omega)

    \\frac{\\partial }{\\partial \\omega} P(z = e^{j \\omega T})
    = \\frac{\\partial }{\\partial \\omega} \\sum_{k = 0}^N c_k e^{-j k \\omega T}
    =  -jT \\sum_{k = 0}^{N} k c_{k} e^{-j k \\omega T}
    =  -jT P_R(z = e^{j \\omega T})

where :math:`P_R` is the "ramped" polynome, i.e. its `k` th coefficient is
multiplied by `k` resp. `k` + 1.

yielding:

.. math::

    \\tau_g(\\omega) = -\\Im \\left\\{ \\frac{H'(\\omega)}{H(\\omega)} \\right\\}
    \\quad \\text{ resp. } \\quad
    \\tau_g(\\omega) = -\\Im \\left\\{ \\frac{H'(e^{j \\omega T})}
                    {H(e^{j \\omega T})} \\right\\}


where::

                    (H'(e^jwT))       (    H_R(e^jwT))        (H_R(e^jwT))
    tau_g(w) = -im  |---------| = -im |-jT ----------| = T re |----------|
                    ( H(e^jwT))       (    H(e^jwT)  )        ( H(e^jwT) )

where :math:`H(e^{j\\omega T})` is calculated via the DFT at NFFT points and
the derivative
of the polynomial terms :math:`b_k z^{-k}` using

.. math::

    \\frac{\\partial} {\\partial \\omega} b_k e^{-jk\\omega T} = -b_k jkT e^{-jk\\omega T}.

This is equivalent to muliplying the polynome with a ramp `k`,
yielding the "ramped" function :math:`H_R(e^{j\\omega T})`.



For analog functions with :math:`b_k s^k` the procedure is analogous, but there is no
sampling time and the exponent is positive.


Examples
--------
>>> b = [1,2,3] # Coefficients of H(z) = 1 + 2 z^2 + 3 z^3
>>> tau_g, td = pyFDA_lib.grpdelay(b)


"""
## If the denominator of the computation becomes too small, the group delay
## is set to zero.  (The group delay approaches infinity when
## there are poles or zeros very close to the unit circle in the z plane.)
##
## Theory: group delay, g(w) = -d/dw [arg{H(e^jw)}],  is the rate of change of
## phase with respect to frequency.  It can be computed as:
##
##               d/dw H(e^-jw)
##        g(w) = -------------
##                 H(e^-jw)
##
## where
##         H(z) = B(z)/A(z) = sum(b_k z^k)/sum(a_k z^k).
##
## By the quotient rule,
##                    A(z) d/dw B(z) - B(z) d/dw A(z)
##        d/dw H(z) = -------------------------------
##                               A(z) A(z)
## Substituting into the expression above yields:
##                A dB - B dA
##        g(w) =  ----------- = dB/B - dA/A
##                    A B
##
## Note that,
##        d/dw B(e^-jw) = sum(k b_k e^-jwk)
##        d/dw A(e^-jw) = sum(k a_k e^-jwk)
## which is just the FFT of the coefficients multiplied by a ramp.
##
## As a further optimization when nfft>>length(a), the IIR filter (b,a)
## is converted to the FIR filter conv(b,fliplr(conj(a))).
    if use_scipy:
        w, gd = sig.group_delay((b,a),w=nfft,whole=whole)
        return w, gd
    if not whole:
        nfft = 2*nfft

#
    w = fs * np.arange(0, nfft)/nfft # create frequency vector
    minmag = 10. * np.spacing(1) # equivalent to matlab "eps"

#    if not use_scipy:
#        try: len(a)
#        except TypeError:
#            a = 1; oa = 0 # a is a scalar or empty -> order of a = 0
#            c = b
#            try: len(b)
#            except TypeError: print('No proper filter coefficients: len(a) = len(b) = 1 !')
#        else:
#            oa = len(a)-1               # order of denom. a(z) resp. a(s)
#            c = np.convolve(b,a[::-1])  # a[::-1] reverses denominator coeffs a
#                                        # c(z) = b(z) * a(1/z)*z^(-oa)
#        try: len(b)
#        except TypeError: b=1; ob=0     # b is a scalar or empty -> order of b = 0
#        else:
#            ob = len(b)-1             # order of b(z)
#
#        if analog:
#            a_b = np.convolve(a,b)
#            if ob > 1:
#                br_a = np.convolve(b[1:] * np.arange(1,ob), a)
#            else:
#                br_a = 0
#            ar_b = np.convolve(a[1:] * np.arange(1,oa), b)
#
#            num = np.fft.fft(ar_b - br_a, nfft)
#            den = np.fft.fft(a_b,nfft)
#        else:
#            oc = oa + ob                  # order of c(z)
#            cr = c * np.arange(0,oc+1) # multiply with ramp -> derivative of c wrt 1/z
#
#            num = np.fft.fft(cr,nfft) #
#            den = np.fft.fft(c,nfft)  #
#    #
#        polebins = np.where(abs(den) < minmag)[0] # find zeros of denominator
#    #    polebins = np.where(abs(num) < minmag)[0] # find zeros of numerator
#        if np.size(polebins) > 0 and verbose:  # check whether polebins array is empty
#            print('*** grpdelay warning: group delay singular -> setting to 0 at:')
#            for i in polebins:
#                print ('f = {0} '.format((fs*i/nfft)))
#                num[i] = 0
#                den[i] = 1
#
#        if analog: # this doesn't work yet
#            tau_g = np.real(num / den)
#        else:
#            tau_g = np.real(num / den) - oa
#    #
#        if not whole:
#            nfft = nfft/2
#            tau_g = tau_g[0:nfft]
#            w = w[0:nfft]
#
#        return w, tau_g
#
#    else:

###############################################################################
#
# group_delay implementation copied and adapted from scipy.signal (0.16)
#
###############################################################################

    if w is None:
        w = 512

    if isinstance(w, int):
        if whole:
            w = np.linspace(0, 2 * pi, w, endpoint=False)
        else:
            w = np.linspace(0, pi, w, endpoint=False)

    w = np.atleast_1d(w)
    b, a = map(np.atleast_1d, (b, a))
    c = np.convolve(b, a[::-1])
    cr = c * np.arange(c.size)
    z = np.exp(-1j * w)
    num = np.polyval(cr[::-1], z)
    den = np.polyval(c[::-1], z)
    singular = np.absolute(den) < 10 * minmag
    if np.any(singular) and verbose:
        singularity_list = ", ".join("{0:.3f}".format(ws/(2*pi)) for ws in w[singular])
        logger.warning("pyfda_lib.py:grpdelay:\n"
            "The group delay is singular at F = [{0:s}], setting to 0".format(singularity_list)
        )

    gd = np.zeros_like(w)
    gd[~singular] = np.real(num[~singular] / den[~singular]) - a.size + 1
    return w, gd

#==================================================================
def expand_lim(ax, eps_x, eps_y = None):
#==================================================================
    """
    Expand the xlim and ylim-values of passed axis by eps

    Parameters
    ----------

    ax : axes object

    eps_x : float
            factor by which x-axis limits are expanded

    eps_y : float
            factor by which y-axis limits are expanded. If eps_y is None, eps_x
            is used for eps_y as well.


    Returns
    -------
    nothing
    """

    if not eps_y:
        eps_y = eps_x
    xmin,xmax,ymin,ymax = ax.axis()
    dx = (xmax - xmin) * eps_x
    dy = (ymax - ymin) * eps_y
    ax.axis((xmin-dx,xmax+dx,ymin-dy,ymax+dy))

#==================================================================
def format_ticks(ax, xy, scale=1., format="%.1f"):
#==================================================================
    """
    Reformat numbers at x or y - axis. The scale can be changed to display
    e.g. MHz instead of Hz. The number format can be changed as well.

    Parameters
    ----------

    ax : axes object

    xy : string, either 'x', 'y' or 'xy'
         select corresponding axis (axes) for reformatting

    scale : real (default: 1.)
            rescaling factor for the axes

    format : string (default: %.1f)
             define C-style number formats

    Returns
    -------
    nothing


    Examples
    --------
    Scale all numbers of x-Axis by 1000, e.g. for displaying ms instead of s.

    >>> format_ticks('x',1000.)

    Two decimal places for numbers on x- and y-axis

    >>> format_ticks('xy',1., format = "%.2f")

    """
    if xy == 'x' or xy == 'xy':
#        locx,labelx = ax.get_xticks(), ax.get_xticklabels() # get location and content of xticks
        locx = ax.get_xticks()
        ax.set_xticks(locx, map(lambda x: format % x, locx*scale))
    if xy == 'y' or xy == 'xy':
        locy = ax.get_yticks() # get location and content of xticks
        ax.set_yticks(locy, map(lambda y: format % y, locy*scale))

#==============================================================================

def fil_save(fil_dict, arg, format_in, sender, convert = True):
    """
    Save filter design ``arg`` given in the format specified as ``format_in`` in
    the dictionary ``fil_dict``. The format can be either poles / zeros / gain,
    filter coefficients (polynomes) or second-order sections.

    Convert the filter design to the other formats if ``convert`` is True.

    Parameters
    ----------

    fil_dict : dict
        The dictionary where the filter design is saved to.

    arg : various formats
        The actual filter design

    format_in : string
        Specifies how the filter design in 'arg' is passed:

        :'ba': Coefficient form: Filter coefficients in FIR format
                 (b, one dimensional) are automatically converted to IIR format (b, a).

        :'zpk': Zero / pole / gain format: When only zeroes are specified,
                  poles and gain are added automatically.

        :'sos': Second-order sections

    sender : string
        The name of the method that calculated the filter. This name is stored
        in ``fil_dict`` together with ``format_in``.

    convert : boolean
        When ``convert = True``, convert arg to the other formats.
    """

    if format_in == 'sos':
            fil_dict['sos'] = arg
            fil_dict['ft'] = 'IIR'

    elif format_in == 'zpk':
        if any(isinstance(el, list) for el in arg):
            frmt = "lol" # list or ndarray or tuple of lists
        elif any(isinstance(el, np.ndarray) for el in arg):
            frmt = "lon" # list or ndarray or tuple of ndarrays
        elif isinstance(arg, list):
            frmt = "lst"
        elif isinstance(arg, np.ndarray):
            frmt = "nd"
        format_error = False
        #logger.error(arg)
        #logger.error(frmt)
        if frmt in {'lst', 'nd'}: # list / array with z only -> FIR
            z = arg
            p = np.zeros(len(z))
            k = 1
            fil_dict['zpk'] = [z, p, k]
            fil_dict['ft'] = 'FIR'
        elif frmt in {'lol', 'lon'}: # list of lists
            if len(arg) == 3:
                fil_dict['zpk'] = [arg[0], arg[1], arg[2]]
                if np.any(arg[1]): # non-zero poles -> IIR
                    fil_dict['ft'] = 'IIR'
                else:
                    fil_dict['ft'] = 'FIR'
            else:
                format_error = True
        else:
            format_error = True


# =============================================================================
#         if np.ndim(arg) == 1:
#             if np.ndim(arg[0]) == 0: # list / array with z only -> FIR
#                 z = arg
#                 p = np.zeros(len(z))
#                 k = 1
#                 fil_dict['zpk'] = [z, p, k]
#                 fil_dict['ft'] = 'FIR'
#             elif np.ndim(arg[0]) == 1: # list of lists
#                 if np.shape(arg)[0] == 3:
#                     fil_dict['zpk'] = [arg[0], arg[1], arg[2]]
#                     if np.any(arg[1]): # non-zero poles -> IIR
#                         fil_dict['ft'] = 'IIR'
#                     else:
#                         fil_dict['ft'] = 'FIR'
#                 else:
#                     format_error = True
#             else:
#                 format_error = True
#         else:
#             format_error = True
#
# =============================================================================
        if format_error:
            raise ValueError("\t'fil_save()': Unknown 'zpk' format {0}".format(arg))


    elif format_in == 'ba':
        if np.ndim(arg) == 1: # arg = [b] -> FIR
            # convert to type array, trim trailing zeros which correspond to
            # (superfluous) highest order polynomial with coefficient 0 as they
            # cause trouble when converting to zpk format
            b = np.trim_zeros(np.asarray(arg))
            a = np.zeros(len(b))
        else: # arg = [b,a]
            b = arg[0]
            a = arg[1]

        if len(b) < 2: # no proper coefficients, initialize with a default
            b = np.asarray([1,0])
        if len(a) < 2: # no proper coefficients, initialize with a default
            a = np.asarray([1,0])

        a[0] = 1 # first coefficient of recursive filter parts always = 1

        # Determine whether it's a FIR or IIR filter and set fil_dict accordingly
        # Test whether all elements except the first one are zero
        if not np.any(a[1:]):
            fil_dict['ft'] = 'FIR'
        else:
            fil_dict['ft'] = 'IIR'

        # equalize if b and a subarrays have different lengths:
        D = len(b) - len(a)
        if D > 0: # b is longer than a -> fill up a with zeros
            a = np.append(a, np.zeros(D))
        elif D < 0: # a is longer than b -> fill up b with zeros
            if fil_dict['ft'] == 'IIR':
                b = np.append(b, np.zeros(-D)) # make filter causal, fill up b with zeros
            else:
                a = a[:D] # discard last D elements of a (only zeros anyway)

        fil_dict['N'] = len(b) - 1 # correct filter order accordingly
        fil_dict['ba'] = [np.array(b, dtype=np.complex), np.array(a, dtype=np.complex)]

    else:
        raise ValueError("\t'fil_save()':Unknown input format {0:s}".format(format_in))

    fil_dict['creator'] = (format_in, sender)
    fil_dict['timestamp'] = time.time()

    # Remove any antiCausal zero/poles
    if 'zpkA' in fil_dict: fil_dict.pop('zpkA')
    if 'baA' in fil_dict: fil_dict.pop('baA')
    if 'rpk' in fil_dict: fil_dict.pop('rpk')

    if convert:
        fil_convert(fil_dict, format_in)

#==============================================================================
def fil_convert(fil_dict, format_in):
    """
    Convert between poles / zeros / gain, filter coefficients (polynomes)
    and second-order sections and store all formats not generated by the filter
    design routine in the passed dictionary ``fil_dict``.

    Parameters
    ----------
    fil_dict :  dict
         filter dictionary containing a.o. all formats to be read and written.

    format_in :  string or set of strings

         format(s) generated by the filter design routine. Must be one of

         :'sos': a list of second order sections - all other formats can easily
                 be derived from this format
         :'zpk': [z,p,k] where z is the array of zeros, p the array of poles and
             k is a scalar with the gain - the polynomial form can be derived
             from this format quite accurately
         :'ba': [b, a] where b and a are the polynomial coefficients - finding
                   the roots of the a and b polynomes may fail for higher orders

    Returns
    -------
    None

    Exceptions
    ----------
    ValueError for Nan / Inf elements or other unsuitable parameters
    """
    if 'sos' in format_in:
        # check for bad coeffs before converting IIR filt
        # this is the same defn used by scipy (tolerance of 1e-14)
        if (fil_dict['ft'] == 'IIR'):
            chk = np.asarray(fil_dict['sos'])
            chk = np.absolute(chk)
            n_sections = chk.shape[0]
            for section in range(n_sections):
                b1 = chk[section, :3]
                a1 = chk[section, 3:]
                if ((np.amin(b1)) < 1e-14 and np.amin(b1) > 0):
                    raise ValueError("\t'fil_convert()': Bad coefficients, Order N is too high!")

        if 'zpk' not in format_in:
            try:
                fil_dict['zpk'] = list(sig.sos2zpk(fil_dict['sos']))
            except Exception as e:
                raise ValueError(e)
            # check whether sos conversion has created a additional (superfluous)
            # pole and zero at the origin and delete them:
            z_0 = np.where(fil_dict['zpk'][0] == 0)[0]
            p_0 = np.where(fil_dict['zpk'][1] == 0)[0]
            if p_0 and z_0: # eliminate z = 0 and p = 0 from list:
                fil_dict['zpk'][0] = np.delete(fil_dict['zpk'][0],z_0)
                fil_dict['zpk'][1] = np.delete(fil_dict['zpk'][1],p_0)

        if 'ba' not in format_in:
            try:
                fil_dict['ba'] = list(sig.sos2tf(fil_dict['sos']))
            except Exception as e:
                raise ValueError(e)
            # check whether sos conversion has created additional (superfluous)
            # highest order polynomial with coefficient 0 and delete them
            if fil_dict['ba'][0][-1] == 0 and fil_dict['ba'][1][-1] == 0:
                fil_dict['ba'][0] = np.delete(fil_dict['ba'][0],-1)
                fil_dict['ba'][1] = np.delete(fil_dict['ba'][1],-1)

    elif 'zpk' in format_in: # z, p, k have been generated,convert to other formats
        zpk = fil_dict['zpk']
        if 'ba' not in format_in:
            try:
                fil_dict['ba'] = sig.zpk2tf(zpk[0], zpk[1], zpk[2])
            except Exception as e:
                raise ValueError(e)
        if 'sos' not in format_in:
            fil_dict['sos'] = [] # don't convert zpk -> SOS due to numerical inaccuracies
#            try:
#                fil_dict['sos'] = sig.zpk2sos(zpk[0], zpk[1], zpk[2])
#            except ValueError:
#                fil_dict['sos'] = []
#                logger.warning("Complex-valued coefficients, could not convert to SOS.")

    elif 'ba' in format_in: # arg = [b,a]
        b, a = fil_dict['ba'][0], fil_dict['ba'][1]
        if np.all(np.isfinite([b,a])):
            zpk = sig.tf2zpk(b,a)
            fil_dict['zpk'] = [np.nan_to_num(zpk[0]).astype(np.complex),
                               np.nan_to_num(zpk[1]).astype(np.complex),
                               np.nan_to_num(zpk[2])
                               ]
        else:
            raise ValueError("\t'fil_convert()': Cannot convert coefficients with NaN or Inf elements to zpk format!")
            zpk = None
        fil_dict['sos'] = [] # don't convert ba -> SOS due to numerical inaccuracies
#        if SOS_AVAIL:
#            try:
#                fil_dict['sos'] = sig.tf2sos(b,a)
#            except ValueError:
#                fil_dict['sos'] = []
#                logger.warning("Complex-valued coefficients, could not convert to SOS.")

    else:
        raise ValueError("\t'fil_convert()': Unknown input format {0:s}".format(format_in))

    # eliminate complex coefficients created by numerical inaccuracies
    fil_dict['ba'] = np.real_if_close(fil_dict['ba'], tol=100) # tol specified in multiples of machine eps

def sos2zpk(sos):
    """
    Taken from scipy/signal/filter_design.py - edit to eliminate first
    order section

    Return zeros, poles, and gain of a series of second-order sections

    Parameters
    ----------
    sos : array_like
        Array of second-order filter coefficients, must have shape
        ``(n_sections, 6)``. See `sosfilt` for the SOS filter format
        specification.

    Returns
    -------
    z : ndarray
        Zeros of the transfer function.
    p : ndarray
        Poles of the transfer function.
    k : float
        System gain.
    Notes
    -----
    .. versionadded:: 0.16.0
    """
    sos = np.asarray(sos)
    n_sections = sos.shape[0]
    z = np.empty(n_sections*2, np.complex128)
    p = np.empty(n_sections*2, np.complex128)
    k = 1.
    for section in range(n_sections):
        logger.info(sos[section])
        zpk = sig.tf2zpk(sos[section, :3], sos[section, 3:])
#        if sos[section, 3] == 0: # first order section
        z[2*section:2*(section+1)] = zpk[0]
#        if sos[section, -1] == 0: # first order section
        p[2*section:2*(section+1)] = zpk[1]
        k *= zpk[2]

    return z, p, k


#------------------------------------------------------------------------------

def round_odd(x):
    """Return the nearest odd integer from x. x can be integer or float."""
    return int(x-np.mod(x,2)+1)


def round_even(x):
    """Return the nearest even integer from x. x can be integer or float."""
    return int(x-np.mod(x,2))


def ceil_odd(x):
    """
    Return the smallest odd integer not less than x. x can be integer or float.
    """
    return round_odd(x+1)

def floor_odd(x):
    """
    Return the largest odd integer not larger than x. x can be integer or float.
    """
    return round_odd(x-1)


def ceil_even(x):
    """
    Return the smallest even integer not less than x. x can be integer or float.
    """
    return round_even(x+1)

def floor_even(x):
    """
    Return the largest even integer not larger than x. x can be integer or float.
    """
    return round_even(x-1)


#------------------------------------------------------------------------------

def calc_Hcomplex(fil_dict, worN, wholeF, fs = 2*np.pi):
    """
    A wrapper around `signal.freqz()` for calculating the complex frequency
    response H(f) for antiCausal systems as well. The filter coefficients are
    are extracted from the filter dictionary.

    Parameters
    ----------

    fil_dict: dict
        dictionary with filter data (coefficients etc.)

    worN: {None, int or array-like}
        number of points or frequencies where the frequency response is calculated

    wholeF: bool
        when True, calculate frequency response from 0 ... f_S, otherwise
        calculate between 0 ... f_S/2

    fs: float
        sampling frequency, used for calculation of the frequency vector.
        The default is 2*pi

    Returns
    -------

    w: ndarray
        The frequencies at which h was computed, in the same units as fs. By default, w is normalized to the range [0, pi) (radians/sample).

    h: ndarray
        The frequency response, as complex numbers.

    Examples
    --------

    """

    # causal poles/zeros
    bc  = fil_dict['ba'][0]
    ac  = fil_dict['ba'][1]

    # standard call to signal freqz
    W, H = sig.freqz(bc, ac, worN = worN, whole = wholeF, fs=fs)

    # test for NonCausal filter
    if ('rpk' in fil_dict):

       # Grab causal, anticausal ba's from dictionary

       ba  = fil_dict['baA'][0]
       aa  = fil_dict['baA'][1]
       ba  = ba.conjugate()
       aa  = aa.conjugate()

       # Evaluate transfer function of anticausal half on the same freq grid.
       # This is done by conjugating a and b prior to the call, and conjugating
       # h after the call.

       wa, ha = sig.freqz(ba, aa, worN = worN, whole=True, fs=fs)
       ha = ha.conjugate()

       # Total transfer function is the product of causal response and antiCausal response

       H = H*ha

    return (W, H)

#------------------------------------------------------------------------------

if __name__=='__main__':
    pass
