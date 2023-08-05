# -*- coding: utf-8 -*-
#
# This file is part of the pyFDA project hosted at https://github.com/chipmuenk/pyfda
#
# Copyright © pyFDA Project Contributors
# Licensed under the terms of the MIT License
# (see file LICENSE in root directory for details)

"""
Library with classes and functions for file and text IO
"""
# TODO: import data from files doesn't update FIR / IIR and data changed

import logging
logger = logging.getLogger(__name__)

import os, re, io
import csv
import datetime

try:
    import cPickle as pickle
except:
    import pickle

import numpy as np
from scipy.io import loadmat, savemat

from .pyfda_lib import safe_eval, lin2unit, pprint_log
from .pyfda_qt_lib import qget_selected, qget_cmb_box, qset_cmb_box, qwindow_stay_on_top

import pyfda.libs.pyfda_fix_lib as fx
from pyfda.pyfda_rc import params
import pyfda.libs.pyfda_dirs as dirs
import pyfda.filterbroker as fb # importing filterbroker initializes all its globals

from .compat import (QLabel, QComboBox, QDialog, QPushButton, QRadioButton, QFD,
                     QFileDialog, QHBoxLayout, QVBoxLayout, QGridLayout, pyqtSignal)
#------------------------------------------------------------------------------
class CSV_option_box(QDialog):
    """
    Create a pop-up widget for setting CSV options. This is needed when storing /
    reading Comma-Separated Value (CSV) files containing coefficients or poles
    and zeros.
    """
    sig_tx = pyqtSignal(dict) # outgoing

    def __init__(self, parent):
        super(CSV_option_box, self).__init__(parent)
        self._construct_UI()
        qwindow_stay_on_top(self, True)

#------------------------------------------------------------------------------
    def closeEvent(self, event):
        """
        Override closeEvent (user has tried to close the window) and send a
        signal to parent where window closing is registered before actually
        closing the window.
        """
        self.sig_tx.emit({'sender':__name__, 'closeEvent':''})
        event.accept()

#------------------------------------------------------------------------------
    def _construct_UI(self):
        """ initialize the User Interface """
        self.setWindowTitle("CSV Options")
        lblDelimiter = QLabel("CSV-Delimiter:", self)
        delim = [('Auto','auto'), ('< , >',','), ('< ; >', ';'), ('<TAB>', '\t'), ('<SPACE>', ' '), ('< | >', '|')]
        self.cmbDelimiter = QComboBox(self)
        for d in delim:
            self.cmbDelimiter.addItem(d[0],d[1])
        self.cmbDelimiter.setToolTip("Delimiter between data fields.")

        lblTerminator = QLabel("Line Terminator:", self)
        terminator = [('Auto','auto'), ('CRLF (Win)', '\r\n'), ('CR (Mac)', '\r'), ('LF (Unix)', '\n'), ('None', '\a')]
        self.cmbLineTerminator = QComboBox(self)
        self.cmbLineTerminator.setToolTip("<span>Terminator at the end of a data row."
                " (depending on the operating system). 'None' can be used for a single "
                "row of data with added line breaks.")
        for t in terminator:
            self.cmbLineTerminator.addItem(t[0], t[1])

        butClose = QPushButton(self)
        butClose.setText("Close")

        lblOrientation = QLabel("Table orientation", self)
        orientation = [('Auto/Horz.', 'auto'), ('Vertical', 'vert'), ('Horizontal', 'horiz')]
        self.cmbOrientation = QComboBox(self)
        self.cmbOrientation.setToolTip("<span>Select orientation of table.</span>")
        for o in orientation:
            self.cmbOrientation.addItem(o[0], o[1])

        lblHeader = QLabel("Enable header", self)
        header = [('Auto', 'auto'), ('On', 'on'), ('Off', 'off')]
        self.cmbHeader = QComboBox(self)
        self.cmbHeader.setToolTip("First row is a header.")
        for h in header:
            self.cmbHeader.addItem(h[0], h[1])

        self.radClipboard = QRadioButton("Clipboard", self)
        self.radClipboard.setChecked(False)
        self.radFile = QRadioButton("File", self)
        self.radFile.setChecked(True) # setting is read later on from params['CSV']['clipboard']

        lay_grid = QGridLayout()
        lay_grid.addWidget(lblDelimiter, 1, 1)
        lay_grid.addWidget(self.cmbDelimiter, 1, 2)
        lay_grid.addWidget(lblTerminator, 2, 1)
        lay_grid.addWidget(self.cmbLineTerminator, 2, 2)
        lay_grid.addWidget(lblOrientation, 3, 1)
        lay_grid.addWidget(self.cmbOrientation, 3, 2)
        lay_grid.addWidget(lblHeader, 4, 1)
        lay_grid.addWidget(self.cmbHeader, 4, 2)
        lay_grid.addWidget(self.radClipboard, 5, 1)
        lay_grid.addWidget(self.radFile, 5, 2)

        layVMain = QVBoxLayout()
        # layVMain.setAlignment(Qt.AlignTop) # this affects only the first widget (intended here)
        layVMain.addLayout(lay_grid)
        layVMain.addWidget(butClose)
        layVMain.setContentsMargins(*params['wdg_margins'])
        self.setLayout(layVMain)

        self._load_settings()

        # ============== Signals & Slots ================================
        butClose.clicked.connect(self.close)
        self.cmbOrientation.currentIndexChanged.connect(self._store_settings)
        self.cmbDelimiter.currentIndexChanged.connect(self._store_settings)
        self.cmbLineTerminator.currentIndexChanged.connect(self._store_settings)
        self.cmbHeader.currentIndexChanged.connect(self._store_settings)
        self.radClipboard.clicked.connect(self._store_settings)
        self.radFile.clicked.connect(self._store_settings)

    def _store_settings(self):
        """
        Store settings of CSV options widget in ``pyfda_rc.params``.
        """

        try:
            params['CSV']['orientation'] =  qget_cmb_box(self.cmbOrientation, data=True)
            params['CSV']['delimiter'] = qget_cmb_box(self.cmbDelimiter, data=True)
            params['CSV']['lineterminator'] = qget_cmb_box(self.cmbLineTerminator, data=True)
            params['CSV']['header'] = qget_cmb_box(self.cmbHeader, data=True)
            params['CSV']['clipboard'] = self.radClipboard.isChecked()

            self.sig_tx.emit({'sender':__name__, 'ui_changed': 'csv'})

        except KeyError as e:
            logger.error(e)

    def _load_settings(self):
        """
        Load settings of CSV options widget from ``pyfda_rc.params``.
        """
        try:
            qset_cmb_box(self.cmbDelimiter, params['CSV']['delimiter'], data=True)
            qset_cmb_box(self.cmbLineTerminator, params['CSV']['lineterminator'], data=True)
            qset_cmb_box(self.cmbHeader, params['CSV']['header'], data=True)
            qset_cmb_box(self.cmbOrientation, params['CSV']['orientation'], data=True)
            self.radClipboard.setChecked(params['CSV']['clipboard'])
            self.radFile.setChecked(not params['CSV']['clipboard'])

        except KeyError as e:
            logger.error(e)
#------------------------------------------------------------------------------
def prune_file_ext(file_type):
    """
    Prune file extension, e.g. '(\*.txt)' from file type description returned
    by QFileDialog. This is achieved with the regular expression

    .. code::

        return = re.sub('\([^\)]+\)', '', file_type)

    Parameters
    ----------
    file_type : str

    Returns
    -------
    str
        The pruned file description

    Notes
    -----
    Syntax of python regex: ``re.sub(pattern, replacement, string)``

    This returns the string obtained by replacing the leftmost non-overlapping
    occurrences of ``pattern`` in ``string`` by ``replacement``.

    - '.' means any character

    - '+' means one or more

    - '[^a]' means except for 'a'

    - '([^)]+)' : match '(', gobble up all characters except ')' till ')'

    - '(' must be escaped as '\\\('

    """



    return re.sub('\([^\)]+\)', '', file_type)

#------------------------------------------------------------------------------
def extract_file_ext(file_type):
    """
    Extract list with file extension(s), e.g. '.vhd' from type description
    (e.g. 'VHDL (\*.vhd)') returned by QFileDialog
    """

    ext_list = re.findall('\([^\)]+\)', file_type) # extract '(*.txt)'
    return [t.strip('(*)') for t in ext_list] # remove '(*)'

#------------------------------------------------------------------------------
def qtable2text(table, data, parent, fkey, frmt='float', title="Export"):
    """
    Transform table to CSV formatted text and copy to clipboard or file

    Parameters
    -----------
    table : object
            Instance of QTableWidget

    data:   object
            Instance of the numpy variable containing table data

    parent: object
            Used to get the clipboard instance from the parent instance (if copying
            to clipboard) or to construct a QFileDialog instance (if copying to a file)

    fkey:  str
            Key for accessing data in ``*.npz`` file or Matlab workspace (``*.mat``)

    frmt: str
           when ``frmt=='float'``, copy data from model, otherwise from the view
           using the ``itemDelegate()`` method of the table.

    comment: str
            comment string indicating the type of data to be copied (e.g.
            "filter coefficients ")


    The following keys from the global dict dict ``params['CSV']`` are evaluated:

    :'delimiter': str (default: ","),
          character for separating columns

    :'lineterminator': str (default: As used by the operating system),
            character for terminating rows. By default,
            the character is selected depending on the operating system:

            - Windows: Carriage return + line feed

            - MacOS  : Carriage return

            - \*nix   : Line feed

    :'orientation': str (one of 'auto', 'horiz', 'vert') determining with which
            orientation the table is written. 'vert' means a line break after 
            each entry or pair of entries which usually is not what you want.
            'auto' doesn't make much sense when writing, 'horiz' is used in this case.

    :'header': str (default: 'auto').
            When ``header='on'``, write the first row with 'b, a'.

    :'clipboard': bool (default: True),
            when ``clipboard = True``, copy data to clipboard, else use a file.

    Returns
    -------
    None
        Nothing, text is exported to clipboard or to file via ``export_data``
    """

    text = ""
    if params['CSV']['header'] in {'auto', 'on'}:
        use_header = True
    elif params['CSV']['header'] == 'off':
        use_header = False
    else:
        logger.error("Unknown key '{0}' for params['CSV']['header']"
                                        .format(params['CSV']['header']))

    if params['CSV']['orientation'] in {'horiz', 'auto'}:
        orientation_horiz = True
    elif params['CSV']['orientation'] == 'vert':
        orientation_horiz = False
    else:
        logger.error("Unknown key '{0}' for params['CSV']['orientation']"
                                        .format(params['CSV']['orientation']))

    delim = params['CSV']['delimiter'].lower()
    if delim == 'auto': # 'auto' doesn't make sense when exporting
        delim = ","
    cr = params['CSV']['lineterminator']

    num_cols = table.columnCount()
    num_rows = table.rowCount()

    sel = qget_selected(table, reverse=False)['sel']

    #============================================================================
    # Nothing selected, but cell format is non-float:
    # -> select whole table, copy all cells further down below:
    #============================================================================
    if not np.any(sel) and frmt != 'float':
        sel = qget_selected(table, reverse=False, select_all = True)['sel']

    #============================================================================
    # Nothing selected, copy complete table from the model (data) in float format:
    #============================================================================
    if not np.any(sel):
        if orientation_horiz: # rows are horizontal
            for c in range(num_cols):
                if use_header: # add the table header
                    text += table.horizontalHeaderItem(c).text() + delim
                for r in range(num_rows):
                    text += str(safe_eval(data[c][r], return_type='auto')) + delim
                text = text.rstrip(delim) + cr
            text = text.rstrip(cr) # delete last CR
        else:  # rows are vertical
            if use_header: # add the table header
                for c in range(num_cols):
                    text += table.horizontalHeaderItem(c).text() + delim
                text = text.rstrip(delim) + cr
            for r in range(num_rows):
                for c in range(num_cols):
                    text += str(safe_eval(data[c][r], return_type='auto')) + delim
                text = text.rstrip(delim) + cr
            text = text.rstrip(cr) # delete CR after last row

    #=======================================================================
    # Copy only selected cells in displayed format:
    #=======================================================================
    else:
        if orientation_horiz: # horizontal orientation, one or two rows
            if use_header: # add the table header
                text += table.horizontalHeaderItem(0).text() + delim
            if sel[0]:
                for r in sel[0]:
                    item = table.item(r,0)
                    if item  and item.text() != "":
                            text += table.itemDelegate().text(item).lstrip(" ") + delim
                text = text.rstrip(delim) # remove last tab delimiter again

            if sel[1]: # returns False for []
                text += cr # add a CRLF when there are two columns
                if use_header: # add the table header
                    text += table.horizontalHeaderItem(1).text() + delim
                for r in sel[1]:
                    item = table.item(r,1)
                    if item and item.text() != "":
                            text += table.itemDelegate().text(item) + delim
                text = text.rstrip(delim) # remove last tab delimiter again
        else: # vertical orientation, one or two columns
            sel_c = []
            if sel[0]:
                sel_c.append(0)
            if sel[1]:
                sel_c.append(1)

            if use_header:
                for c in sel_c:
                    text += table.horizontalHeaderItem(c).text() + delim
                    # cr is added further below
                text.rstrip(delim)

            for r in range(num_rows): # iterate over whole table
                for c in sel_c:
                    if r in sel[c]: # selected item?
                        item = table.item(r,c)
                        # print(c,r)
                        if item and item.text() != "":
                            text += table.itemDelegate().text(item).lstrip(" ") + delim
                text = text.rstrip(delim) + cr
            text.rstrip(cr)

    if params['CSV']['clipboard']:
        fb.clipboard.setText(text)
    else:
        export_data(parent, text, fkey, title=title)

#==============================================================================
#     # Here 'a' is the name of numpy array and 'file' is the variable to write in a file.
#     ##if you want to write in column:
#
#     for x in np.nditer(a.T, order='C'):
#             file.write(str(x))
#             file.write("\n")
#
#     ## If you want to write in row: ##
#
#     writer= csv.writer(file, delimiter=',')
#     for x in np.nditer(a.T, order='C'):
#             row.append(str(x))
#     writer.writerow(row)
#
#==============================================================================


#------------------------------------------------------------------------------
def qtext2table(parent, fkey, title = "Import"):
    """
    Copy data from clipboard or file to table

    Parameters
    -----------

    parent: object
            parent instance, having a QClipboard and / or a QFileDialog attribute.

    fkey: str
            Key for accessing data in *.npz file or Matlab workspace (*.mat)

    title: str
        title string for the file dialog box


    The following keys from the global dict ``params['CSV']`` are evaluated:

    :'delimiter': str (default: <tab>), character for separating columns

    :'lineterminator': str (default: As used by the operating system),
            character for terminating rows. By default,
            the character is selected depending on the operating system:

            - Windows: Carriage return + line feed

            - MacOS  : Carriage return

            - \*nix   : Line feed

    :'orientation': str (one of 'auto', 'horiz', 'vert') determining with which
            orientation the table is read.

    :'header': str (**'auto'**, 'on', 'off').
            When ``header=='on'``, treat first row as a header that will be discarded.

    :'clipboard': bool (default: True).
            When ``clipboard == True``, copy data from clipboard, else use a file

    Parameters that are 'auto', will be guessed by ``csv.Sniffer()``.

    Returns
    --------
    ndarray of str
        table data
    """

    if params['CSV']['clipboard']: # data from clipboard
        text = fb.clipboard.text()
        logger.debug("Importing data from clipboard:\n{0}\n{1}".format(np.shape(text), text))
        # pass handle to text and convert to numpy array:
        data_arr = csv2array(io.StringIO(text))
        if isinstance(data_arr, str): # returned an error message instead of numpy data
            logger.error("Error importing clipboard data:\n\t{0}".format(data_arr))
            return None
    else: # data from file
        data_arr = import_data(parent, fkey, title=title)
        # pass data as numpy array
        logger.debug("Imported data from file. shape = {0} | {1}\n{2}".format(np.shape(data_arr), np.ndim(data_arr), data_arr))
        if type(data_arr) == int and data_arr == -1: # file operation cancelled
            data_arr = None
    return data_arr


#------------------------------------------------------------------------------
def csv2array(f):
    """
    Convert comma-separated values from file or text
    to numpy array, taking into accout the settings of the CSV dict.

    Parameters
    ----------

    f: handle to file or file-like object
        e.g.

        >>> f = open(file_name, 'r') # or
        >>> f = io.StringIO(text)

    Returns
    -------

    ndarray
        numpy array containing table data from file or text when import was
        successful

    io_error: str
        String with the error message when import was unsuccessful
    """
    #------------------------------------------------------------------------------
    # Get CSV parameter settings
    #------------------------------------------------------------------------------
    io_error = "" # initialize string for I/O error messages
    CSV_dict = params['CSV']
    try:
        header = CSV_dict['header'].lower()
        if header in {'auto', 'on', 'off'}:
            pass
        else:
            header = 'auto'
            logger.warning("Unknown key '{0}' for CSV_dict['header'], using {1} instead."
                                            .format(CSV_dict['header']), header)

        orientation_horiz = CSV_dict['orientation'].lower()
        if orientation_horiz in {'auto', 'vert', 'horiz'}:
            pass
        else:
            orientation_horiz = 'vert'
            logger.warning("Unknown key '{0}' for CSV_dict['orientation'], using {1} instead."
                                        .format(CSV_dict['orientation']), orientation_horiz)

        tab = CSV_dict['delimiter'].lower()
        cr = CSV_dict['lineterminator'].lower()

    except KeyError as e:
        io_error = "Dict 'params':\n{0}".format(e)
        return io_error

    try:
        #------------------------------------------------------------------------------
        # Analyze CSV object
        #------------------------------------------------------------------------------
        if header == 'auto' or tab == 'auto' or cr == 'auto':
        # test the first line for delimiters (of the given selection)
            dialect = csv.Sniffer().sniff(f.readline(), delimiters=['\t',';',',', '|', ' '])
            f.seek(0)                               # and reset the file pointer
        else:
            dialect = csv.get_dialect('excel-tab') # fall back, alternatives: 'excel', 'unix'

        if header == "auto":
            use_header = csv.Sniffer().has_header(f.read(1000)) # True when header detected
            f.seek(0)

    except csv.Error as e:
        logger.warning("Error during CSV analysis:\n{0},\n"
                       "continuing with format 'excel-tab'".format(e))
        dialect = csv.get_dialect('excel-tab') # fall back
        use_header = False

    if header == 'on':
        use_header = True
    if header == 'off':
        use_header = False
    # case 'auto' has been treated above

    delimiter = dialect.delimiter
    lineterminator = dialect.lineterminator
    quotechar = dialect.quotechar

    if tab != 'auto':
        delimiter = str(tab)

    if cr != 'auto':
        lineterminator = str(cr)

    logger.info("Parsing CSV data with \n"
                "\tHeader = {0} | Delim. = {1} | Lineterm. = {2} | Quotechar = ' {3} '"
                #"\n\tType of passed text: '{4}'"
                .format(use_header, repr(delimiter), repr(lineterminator),
                        quotechar))#,f.__class__.__name__))
    #------------------------------------------------
    # finally, create iterator from csv data
    data_iter = csv.reader(f, dialect=dialect, delimiter=delimiter, lineterminator=lineterminator) # returns an iterator
    #------------------------------------------------
# =============================================================================
#     with open('/your/path/file') as f:
#         for line in f:
#             process(line)
#
#     Where you define your process function any way you want. For example:
#
#         def process(line):
#             if 'save the world' in line.lower():
#                 superman.save_the_world()
#
#     This will work nicely for any file size and you go through your file in just 1 pass.
#     This is typically how generic parsers will work.
#     (https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list)
# =============================================================================

    if use_header:
        logger.info("Headers:\n{0}".format(next(data_iter, None))) # py3 and py2

    data_list = []
    try:
        for row in data_iter:
            logger.debug("{0}".format(row))
            data_list.append(row)
    except csv.Error as e:
        io_error = "Error during CSV reading:\n{0}".format(e)
        return io_error

    try:
        if data_list is None:
            return "Imported data is None."           
        data_arr = np.array(data_list)
        if np.ndim(data_arr) == 0 or (np.ndim(data_arr) == 1 and len(data_arr) < 2):
            return "Imported data is a scalar: '0'".format(data_arr)
        elif np.ndim(data_arr) == 1:
            return data_arr
        elif np.ndim(data_arr) == 2:
            cols, rows = np.shape(data_arr)
            logger.debug("cols = {0}, rows = {1}, data_arr = {2}\n".format(cols, rows, data_arr))
            if cols > 2 and rows > 2:
                return "Unsuitable data shape {0}".format(np.shape(data_arr))
            elif cols > rows:
                return data_arr.T
            else:
                return data_arr
        else:
            return "Unsuitable data shape: ndim = {0}, shape = {1}"\
                .format(np.ndim(data_arr), np.shape(data_arr))

    except (TypeError, ValueError) as e:
        io_error = "{0}\nFormat = {1}\n{2}".format(e, np.shape(data_arr), data_list)
        return io_error

# =============================================================================
#     try:
#         data_arr = np.array(data_list)
#         cols, rows = np.shape(data_arr)
#         logger.debug("cols = {0}, rows = {1}, data_arr = {2}\n".format(cols, rows, data_arr))
#         if params['CSV']['orientation'] == 'vert':
#             return data_arr.T
#         else:
#             return data_arr
# 
#     except (TypeError, ValueError) as e:
#         io_error = "{0}\nFormat = {1}\n{2}".format(e, np.shape(data_arr), data_list)
#         return io_error
# 
# =============================================================================
#------------------------------------------------------------------------------
def csv2array_new(f):
    """
    Convert comma-separated values from file or text
    to numpy array, taking into accout the settings of the CSV dict.

    Parameters
    ----------

    f: handle to file or file-like object
        e.g.

        >>> f = open(file_name, 'r') # or
        >>> f = io.StringIO(text)

    Returns
    -------

    ndarray
        numpy array containing table data from file or text when import was
        successful

    io_error: str
        String with the error message when import was unsuccessful
    """
    #------------------------------------------------------------------------------
    # Get CSV parameter settings
    #------------------------------------------------------------------------------
    io_error = "" # initialize string for I/O error messages
    CSV_dict = params['CSV']
    logger.warning("Fileobject format: {0}".format(type(f).__name__))
    try:
        header = CSV_dict['header'].lower()
        if header in {'auto', 'on', 'off'}:
            pass
        else:
            header = 'auto'
            logger.warning("Unknown key '{0}' for CSV_dict['header'], using {1} instead."
                                            .format(CSV_dict['header']), header)

        orientation_horiz = CSV_dict['orientation'].lower()
        if orientation_horiz in {'auto', 'vert', 'horiz'}:
            pass
        else:
            orientation_horiz = 'vert'
            logger.warning("Unknown key '{0}' for CSV_dict['orientation'], using {1} instead."
                                        .format(CSV_dict['orientation']), orientation_horiz)

        tab = CSV_dict['delimiter'].lower()
        cr = CSV_dict['lineterminator'].lower()

    except KeyError as e:
        io_error = "Dict 'params':\n{0}".format(e)
        return io_error

    try:
        #------------------------------------------------------------------------------
        # Analyze CSV object
        #------------------------------------------------------------------------------
        if header == 'auto' or tab == 'auto' or cr == 'auto':
        # test the first line for delimiters (of the given selection)
            dialect = csv.Sniffer().sniff(f.readline(), delimiters=['\t',';',',', '|', ' '])
            f.seek(0)                               # and reset the file pointer
        else:
            dialect = csv.get_dialect('excel-tab') # fall back, alternatives: 'excel', 'unix'

        if header == "auto":
            use_header = csv.Sniffer().has_header(f.read(1000)) # True when header detected
            f.seek(0)

    except csv.Error as e:
        logger.warning("Error during CSV analysis:\n{0},\n"
                       "continuing with format 'excel-tab'".format(e))
        dialect = csv.get_dialect('excel-tab') # fall back
        use_header = False

    if header == 'on':
        use_header = True
    elif header == 'off':
        use_header = False
    # case 'auto' has been treated above

    delimiter = dialect.delimiter
    lineterminator = dialect.lineterminator
    quotechar = dialect.quotechar

    if tab != 'auto':
        delimiter = str(tab)

    if cr != 'auto':
        lineterminator = str(cr)

    logger.info("Parsing CSV data with header = '{0}'\n"
                "\tDelimiter = {1} | Lineterm. = {2} | quotechar = ' {3} '\n"
                "\tType of passed text: '{4}'"
                .format(use_header, repr(delimiter), repr(lineterminator),
                        quotechar,f.__class__.__name__))
    #------------------------------------------------
    # finally, create iterator from csv data
    data_iter = csv.reader(f, dialect=dialect, delimiter=delimiter, lineterminator=lineterminator)
    #------------------------------------------------
# =============================================================================
    """ 
    newline controls how universal newlines works (it only applies to text mode). 
    It can be None, '', '\n', '\r', and '\r\n'. It works as follows:

    - On input, if newline is None, universal newlines mode is enabled. Lines in 
      the input can end in '\n', '\r', or '\r\n', and these are translated into
      '\n' before being returned to the caller. If it is '', universal newline
      mode is enabled, but line endings are returned to the caller untranslated.
      If it has any of the other legal values, input lines are only terminated 
      by the given string, and the line ending is returned to the caller untranslated.

    - On output, if newline is None, any '\n' characters written are translated 
      to the system default line separator, os.linesep. If newline is '', 
      no translation takes place. If newline is any of the other legal values, 
      any '\n' characters written are translated to the given string.
      
      Example: convert from Windows-style line endings to Linux:
      fileContents = open(filename,"r").read()
      f = open(filename,"w", newline="\n")
      f.write(fileContents)
      f.close()
      https://pythonconquerstheuniverse.wordpress.com/2011/05/08/newline-conversion-in-python-3/
     """

    data_list = []
    
    def process(line):
        data_list.append(line.split(lineterminator)) # split into lines (if not split yet)


    #with open(fo) as f:
    for line in f:
        process(line)
        
    for e in data_list:
        pass
        

    # Where you define your process function any way you want. For example:


    # This will work nicely for any file size and you go through your file in just 1 pass.
    # This is typically how generic parsers will work.
    # (https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list)
# =============================================================================

# =============================================================================
#     if use_header:
#         logger.info("Headers:\n{0}".format(next(data_iter, None))) # py3 and py2
# 
#     try:
#         for row in data_iter:
#             logger.debug("{0}".format(row))
#             data_list.append(row)
#     except csv.Error as e:
#         io_error = "Error during CSV reading:\n{0}".format(e)
#         return io_error
# =============================================================================

    try:
        if data_list is None:
            return "Imported data is None."           
        data_arr = np.array(data_list)
        if np.ndim(data_arr) == 0 or (np.ndim(data_arr) == 1 and len(data_arr) < 2):
            return "Imported data is a scalar: '0'".format(data_arr)
        elif np.ndim(data_arr) == 1:
            return data_arr
        elif np.ndim(data_arr) == 2:
            cols, rows = np.shape(data_arr)
            logger.debug("cols = {0}, rows = {1}, data_arr = {2}\n".format(cols, rows, data_arr))
            if cols > 2 and rows > 2:
                return "Unsuitable data shape {0}".format(np.shape(data_arr))
            elif cols > rows:
                return data_arr.T
            else:
                return data_arr
        else:
            return "Unsuitable data shape: ndim = {0}, shape = {1}"\
                .format(np.ndim(data_arr), np.shape(data_arr))

    except (TypeError, ValueError) as e:
        io_error = "{0}\nFormat = {1}\n{2}".format(e, np.shape(data_arr), data_list)
        return io_error


#------------------------------------------------------------------------------
def import_data(parent, fkey, title="Import"):
    """
    Import data from a file and convert it to a numpy array.

    Parameters
    ----------
    parent: handle to calling instance

    fkey: str
        Key for accessing data in *.npz or Matlab workspace (*.mat) file with
        multiple entries.

    title: str
        title string for the file dialog box (e.g. "filter coefficients ")

    Returns
    -------
    ndarray
        Data from the file
    """
    file_filters = ("Comma / Tab Separated Values (*.csv *.txt);;"
                    "Matlab-Workspace (*.mat);;"
    "Binary Numpy Array (*.npy);;Zipped Binary Numpy Array(*.npz)")
    dlg = QFileDialog(parent) # create instance for QFileDialog
    dlg.setWindowTitle(title)
    dlg.setDirectory(dirs.save_dir)
    dlg.setAcceptMode(QFileDialog.AcceptOpen) # set dialog to "file open" mode
    dlg.setNameFilter(file_filters)
    dlg.setDefaultSuffix('csv') # default suffix when none is given
    dlg.selectNameFilter(dirs.save_filt) # default filter selected in file dialog

    if dlg.exec_() == QFileDialog.Accepted:
        file_name = dlg.selectedFiles()[0] # pick only first selected file
        file_type = os.path.splitext(file_name)[1]
        sel_filt = '*' + file_type
        #sel_filt = dlg.selectedNameFilter()
    else:
        return -1  # operation cancelled

    # strip extension from returned file name (if any) + append file type:
    #file_name = os.path.splitext(file_name)[0] + file_type
    
    logger.info('Try to import file \n\t"{0}"'.format(file_name))

    file_type_err = False
    try:
        if file_type in {'.csv', '.txt'}:
            with open(file_name, 'r', newline=None) as f:
                data_arr = csv2array(f)
                # data_arr = np.loadtxt(f, delimiter=params['CSV']['delimiter'].lower())
                if isinstance(data_arr, str): # returned an error message instead of numpy data
                    logger.error("Error loading file '{0}':\n{1}".format(file_name, data_arr))
                    return None
        else:
            with open(file_name, 'rb') as f:
                if file_type == '.mat':
                    data_arr = loadmat(f)[fkey]
                elif file_type == '.npy':
                    data_arr = np.load(f)
                    # contains only one array
                elif file_type == '.npz':
                    fdict = np.load(f)
                    if fkey not in fdict:
                        file_type_err = True
                        raise IOError("Key '{0}' not in file '{1}'.\nKeys found: {2}"\
                                     .format(fkey, file_name, fdict.files))
                    else:
                        data_arr = fdict[fkey] # pick the array `fkey` from the dict
                else:
                    logger.error('Unknown file type "{0}"'.format(file_type))
                    file_type_err = True

        if not file_type_err:
            logger.info("Success! Parsed data format:\n{0}".format(pprint_log(data_arr,N=3)))
            dirs.save_dir = os.path.dirname(file_name)
            dirs.save_filt = sel_filt
            return data_arr # returns numpy array

    except IOError as e:
        logger.error("Failed loading {0}!\n{1}".format(file_name, e))
        return None

#------------------------------------------------------------------------------
def export_data(parent, data, fkey, title="Export"):
    """
    Export coefficients or pole/zero data in various formats

    Parameters
    ----------
    parent: handle to calling instance for creating file dialog instance

    data: str
        formatted as CSV data, i.e. rows of elements separated by 'delimiter',
        terminated by 'lineterminator'

    fkey: str
        Key for accessing data in ``*.npz`` or Matlab workspace (``*.mat``) file.
        When fkey == 'ba', exporting to FPGA coefficients format is enabled.

    title: str
        title string for the file dialog box (e.g. "filter coefficients ")

    """

    logger.debug("imported data: type{0}|dim{1}|shape{2}\n{3}"\
                   .format(type(data), np.ndim(data), np.shape(data), data))

    file_filters = ("Comma / Tab Separated Values (*.csv);;"
                    "Matlab-Workspace (*.mat);;"
        "Binary Numpy Array (*.npy);;Zipped Binary Numpy Array (*.npz)")

    if fb.fil[0]['ft'] == 'FIR':
        file_filters += (";;Xilinx FIR coefficient format (*.coe)"
                         ";;Microsemi FIR coefficient format (*.txt)"
                         ";;VHDL Package (*.vhd)")

#        # Add further file types when modules are available:
#        if XLWT:
#            file_filters += ";;Excel Worksheet (.xls)"
#        if XLSX:
#            file_filters += ";;Excel 2007 Worksheet (.xlsx)"

    # return selected file name (with or without extension) and filter (Linux: full text)
    dlg = QFileDialog(parent) # create instance for QFileDialog
    dlg.setWindowTitle(title)
    dlg.setDirectory(dirs.save_dir)
    dlg.setAcceptMode(QFileDialog.AcceptSave) # set dialog to "file save" mode
    dlg.setNameFilter(file_filters)
    # dlg.setDefaultSuffix('csv') # default suffix when none is given
    dlg.selectNameFilter(dirs.save_filt) # default file type selected in file dialog

    if dlg.exec_() == QFileDialog.Accepted:
        file_name = dlg.selectedFiles()[0] # pick only first selected file
        sel_filt = dlg.selectedNameFilter()
    else:
        return -1

    for t in extract_file_ext(file_filters): # extract the list of file extensions
        if t in str(sel_filt):
            file_type = t

    # strip extension from returned file name (if any) + append file type:
    file_name = os.path.splitext(file_name)[0] +  file_type
    file_type_err = False

    try:
        if file_type in {'.csv'}:
            with open(file_name, 'w', encoding="utf8", newline='') as f:
                f.write(data)
        elif file_type in {'.coe', '.txt', '.vhd'}: # text / string format
            with open(file_name, 'w', encoding="utf8") as f:
                if file_type == '.coe':
                    err = export_coe_xilinx(f)
                elif file_type == '.txt':
                    err = export_coe_microsemi(f)
                else: #file_type == '.vhd':
                    err = export_coe_vhdl_package(f)

        else: # binary format
            # convert csv data to numpy array
            np_data = csv2array(io.StringIO(data))
            if isinstance(np_data, str): # returned an error message instead of numpy data
                logger.error("Error converting coefficient data:\n{0}".format(np_data))
                return None

            with open(file_name, 'wb') as f:
                if file_type == '.mat':
                    savemat(f, mdict={fkey:np_data})
                    # newline='\n', header='', footer='', comments='# ', fmt='%.18e'
                elif file_type == '.npy':
                    # can only store one array in the file, no pickled data
                    # for Py2 <-> 3 compatibility
                    np.save(f, np_data, allow_pickle=False)
                elif file_type == '.npz':
                    # would be possible to store multiple arrays in the file
                    fdict = {fkey:np_data}
                    np.savez(f, **fdict) # unpack kw list (only one here)
                elif file_type == '.xls':
                    # see
                    # http://www.dev-explorer.com/articles/excel-spreadsheets-and-python
                    # https://github.com/python-excel/xlwt/blob/master/xlwt/examples/num_formats.py
                    # http://reliablybroken.com/b/2011/07/styling-your-excel-data-with-xlwt/
                    workbook = xlwt.Workbook(encoding="utf-8")
                    worksheet = workbook.add_sheet("Python Sheet 1")
                    bold = xlwt.easyxf('font: bold 1')
                    worksheet.write(0, 0, 'b', bold)
                    worksheet.write(0, 1, 'a', bold)
                    for col in range(2):
                        for row in range(np.shape(data)[1]):
                            worksheet.write(row+1, col, data[col][row]) # vertical
                    workbook.save(f)

                elif file_type == '.xlsx':
                    # from https://pypi.python.org/pypi/XlsxWriter
                    # Create an new Excel file and add a worksheet.
                    workbook = xlsx.Workbook(f)
                    worksheet = workbook.add_worksheet()
                    # Widen the first column to make the text clearer.
                    worksheet.set_column('A:A', 20)
                    # Add a bold format to use to highlight cells.
                    bold = workbook.add_format({'bold': True})
                    # Write labels with formatting.
                    worksheet.write('A1', 'b', bold)
                    worksheet.write('B1', 'a', bold)

                    # Write some numbers, with row/column notation.
                    for col in range(2):
                        for row in range(np.shape(data)[1]):
                            worksheet.write(row+1, col, data[col][row]) # vertical
        #                    worksheet.write(row, col, coeffs[col][row]) # horizontal

                    # Insert an image - useful for documentation export ?!.
        #            worksheet.insert_image('B5', 'logo.png')

                    workbook.close()

                else:
                    logger.error('Unknown file type "{0}"'.format(file_type))
                    file_type_err = True

        if not file_type_err:
            logger.info('Filter saved as\n\t"{0}"'.format(file_name))
            dirs.save_dir = os.path.dirname(file_name) # save new dir
            dirs.save_filt = sel_filt # save new filter selection

    except IOError as e:
        logger.error('Failed saving "{0}"!\n{1}\n'.format(file_name, e))


        # Download the Simple ods py module:
        # http://simple-odspy.sourceforge.net/
        # http://codextechnicanum.blogspot.de/2014/02/write-ods-for-libreoffice-calc-from_1.html

#------------------------------------------------------------------------------
def generate_header(title):

    f_lbls = []
    f_vals = []
    a_lbls = []
    a_targs = []
    a_targs_dB = []
    ft = fb.fil[0]['ft'] # get filter type ('IIR', 'FIR')
    unit = fb.fil[0]['amp_specs_unit']
    unit = 'dB' # fix this for the moment
    # construct pairs of corner frequency and corresponding amplitude
    # labels in ascending frequency for each response type
    if fb.fil[0]['rt'] in {'LP', 'HP', 'BP', 'BS', 'HIL'}:
        if fb.fil[0]['rt'] == 'LP':
            f_lbls = ['F_PB', 'F_SB']
            a_lbls = ['A_PB', 'A_SB']
        elif fb.fil[0]['rt'] == 'HP':
            f_lbls = ['F_SB', 'F_PB']
            a_lbls = ['A_SB', 'A_PB']
        elif fb.fil[0]['rt'] == 'BP':
            f_lbls = ['F_SB', 'F_PB', 'F_PB2', 'F_SB2']
            a_lbls = ['A_SB', 'A_PB', 'A_PB', 'A_SB2']
        elif fb.fil[0]['rt'] == 'BS':
            f_lbls = ['F_PB', 'F_SB', 'F_SB2', 'F_PB2']
            a_lbls = ['A_PB', 'A_SB', 'A_SB', 'A_PB2']
        elif fb.fil[0]['rt'] == 'HIL':
            f_lbls = ['F_PB', 'F_PB2']
            a_lbls = ['A_PB', 'A_PB']


    # Try to get lists of frequency / amplitude specs from the filter dict
    # that correspond to the f_lbls / a_lbls pairs defined above
    # When one of the labels doesn't exist in the filter dict, delete
    # all corresponding amplitude and frequency entries.
        err = [False] * len(f_lbls) # initialize error list
        f_vals = []
        a_targs = []
        for i in range(len(f_lbls)):
            try:
                f = fb.fil[0][f_lbls[i]]
                f_vals.append(f)
            except KeyError as e:
                f_vals.append('')
                err[i] = True
                logger.debug(e)
            try:
                a = fb.fil[0][a_lbls[i]]
                a_dB = lin2unit(fb.fil[0][a_lbls[i]], ft, a_lbls[i], unit)
                a_targs.append(a)
                a_targs_dB.append(a_dB)
            except KeyError as e:
                a_targs.append('')
                a_targs_dB.append('')
                err[i] = True
                logger.debug(e)

        for i in range(len(f_lbls)):
            if err[i]:
                del f_lbls[i]
                del f_vals[i]
                del a_lbls[i]
                del a_targs[i]
                del a_targs_dB[i]

    date_frmt = "%d-%B-%Y %H:%M:%S" # select date format
    unit = fb.fil[0]['plt_fUnit']
    if unit in {'f_S', 'f_Ny'}:
        f_S = ""
    else:
        f_S = fb.fil[0]["f_S"]
    header = (
        "------------------------------------------------------------------------------------\n"
        "\n"
        "{0}".format(title) + "\n"
        "Generated by pyFDA 0.3 (https://github.com/chipmuenk/pyfda)\n\n")
    header += "Designed:\t{0}\n".format(datetime.datetime.fromtimestamp(int(fb.fil[0]['timestamp'])).strftime(date_frmt))
    header += "Saved:\t{0}\n\n".format(datetime.datetime.now().strftime(date_frmt))
    header += "Filter type:\t{0}, {1} (Order = {2})\n".format( fb.fil[0]['rt'], fb.fil[0]['fc'], fb.fil[0]["N"])
    header += "Sample Frequency \tf_S = {0} {1}\n\n".format(f_S, unit)
    header += "Corner Frequencies:\n"
    for lf,f,la,a in zip(f_lbls, f_vals, a_lbls, a_targs_dB):
        header += "\t" + lf + " = " + str(f) + " " + unit + " : " + la + " = " + str(a) +" dB\n"
    header += "------------------------------------------------------------------------------------\n"
    return header

#------------------------------------------------------------------------------
def export_coe_xilinx(f):
    """
    Save FIR filter coefficients in Xilinx coefficient format as file '\*.coe', specifying
    the number base and the quantized coefficients (decimal or hex integer).
    """
    qc = fx.Fixed(fb.fil[0]['fxqc']['QCB']) # instantiate fixpoint object
    logger.debug("scale = {0}, WF = {1}".format(qc.scale, qc.WF))

    if qc.WF != 0: # Set the fixpoint format to integer (WF=0) with the original wordlength
        qc.setQobj({'W':qc.W, 'scale':1 << qc.W-1})# Set the fixpoint format to integer (WF=0) with the original wordlength
        logger.warning("Fractional formats are not supported, using integer format.")

    if qc.frmt == 'hex': # select hex format
        coe_radix = 16
    if qc.frmt == 'bin': # select binary format
        coe_radix = 2        
    else:
        logger.warning('Coefficients in "{0}" format are not supported in COE files, '
                       'using decimal format.')
        qc.setQobj({'frmt':'dec'}) # select decimal format in all other cases
        coe_radix = 10

    # Quantize coefficients to decimal / hex integer format, returning an array of strings
    bq = qc.float2frmt(fb.fil[0]['ba'][0])

    exp_str = "; " + generate_header("XILINX CORE Generator(tm) Distributed Arithmetic FIR filter coefficient (.COE) file").replace("\n","\n; ")

    exp_str += "\nRadix = {0};\n".format(coe_radix)
    exp_str += "Coefficient_width = {0};\n".format(qc.W) # quantized wordlength
    coeff_str = "CoefData = "
    for b in bq:
        coeff_str += str(b) + ",\n"
    exp_str += coeff_str[:-2] + ";" # replace last "," by ";"

    f.write(exp_str)

#------------------------------------------------------------------------------
def export_coe_microsemi(f):
    """
    Save FIR filter coefficients in Actel coefficient format as file '\*.txt'.
    Coefficients have to be in integer format, the last line has to be empty.
    For (anti)aymmetric filter only one half of the coefficients must be
    specified?
    """
    qc = fx.Fixed(fb.fil[0]['fxqc']['QCB']) # instantiate fixpoint object

    if qc.WF != 0: # Set the fixpoint format to integer (WF=0) with the original wordlength:
        qc.setQobj({'W':qc.W, 'scale':1 << qc.W-1})
        logger.warning("Fractional formats are not supported, using integer format.")

    if qc.frmt != 'dec':
        qc.setQobj({'frmt':'dec'}) # select decimal format in all other cases
        logger.warning('Only coefficients in "dec" format are supported,'
                       'using decimal format.')

    # Quantize coefficients to decimal integer format, returning an array of strings
    bq = qc.float2frmt(fb.fil[0]['ba'][0])

    coeff_str = "coefficient_set_1\n"
    for b in bq:
        coeff_str += str(b) + "\n"

    f.write(coeff_str)
    
    return None

#------------------------------------------------------------------------------
def export_coe_vhdl_package(f):
    """
    Save FIR filter coefficients as a VHDL package '\*.vhd', specifying
    the number base and the quantized coefficients (decimal or hex integer).
    """
    qc = fx.Fixed(fb.fil[0]['fxqc']['QCB']) # instantiate fixpoint object
    if not qc.frmt == 'float' and qc.WF != 0: 
        # Set the fixpoint format to integer (WF=0) with the original wordlength
        qc.setQobj({'W':qc.W, 'scale':1 << qc.W-1})
        logger.warning("Fractional formats are not supported, using integer format.")

    WO = fb.fil[0]['fxqc']['QO']['W']

    if qc.frmt == 'hex':
        pre = "#16#"
        post = "#"
    elif qc.frmt =='bin':
        pre = "#2#"
        post = "#"
    elif qc.frmt in {'dec', 'float'}:
        pre = ""
        post = ""    
    else:
        qc.setQobj({'frmt':'dec'}) # select decimal format in all other cases
        pre = ""
        post = ""    
        logger.warning('Coefficients in "{0}" format are currently not supported, '
                       'using decimal format.'.format(qc.frmt))
        
    # Quantize coefficients to selected fixpoint format, returning an array of strings
    bq = qc.float2frmt(fb.fil[0]['ba'][0])

    exp_str = "-- " + generate_header("VHDL FIR filter coefficient package file").replace("\n","\n-- ")

    exp_str += "\nlibrary IEEE;\n"
    if qc.frmt == 'float':
        exp_str += "use IEEE.math_real.all;\n"
    exp_str += "USE IEEE.std_logic_1164.all;\n\n"
    exp_str += "package coeff_package is\n"
    exp_str += "constant n_taps: integer := {0:d};\n".format(len(bq)-1)
    if qc.frmt == 'float':
        exp_str += "type coeff_type is array(0 to n_taps) of real;\n"
    else:
        exp_str += "type coeff_type is array(0 to n_taps) of integer "        
        exp_str += "range {0} to {1};\n\n".format(-1 << WO-1, (1 << WO-1) - 1)
    exp_str += "constant coeff : coeff_type := "

    coeff_str = "(\n"
    for b in bq:
        coeff_str += "\t" + pre + str(b) + post + ",\n"
    exp_str += coeff_str[:-2] + ");\n\n" # replace last "," by ");"

    exp_str += "end coeff_package;"

    f.write(exp_str)
    
    return None

#------------------------------------------------------------------------------
def export_coe_TI(f):
    """
    Save FIR filter coefficients in TI coefficient format
    Coefficient have to be specified by an identifier 'b0 ... b191' followed
    by the coefficient in normalized fractional format, e.g.

    b0 .053647
    b1 -.27485
    b2 .16497
    ...

    ** not implemented yet **
    """
    pass

#------------------------------------------------------------------------------

#==============================================================================

def load_filter(self):
    """
    Load filter from zipped binary numpy array or (c)pickled object to
    filter dictionary and update input and plot widgets
    """
    file_filters = ("Zipped Binary Numpy Array (*.npz);;Pickled (*.pkl)")
    dlg = QFD(self)
    file_name, file_type = dlg.getOpenFileName_(
            caption = "Load filter ", directory = dirs.save_dir,
            filter = file_filters)
    file_name = str(file_name) # QString -> str

    for t in extract_file_ext(file_filters): # get a list of file extensions
        if t in str(file_type):
            file_type = t

    if file_name != "": # cancelled file operation returns empty string
        if os.stat(file_name).st_size == 0:
            dirs.save_dir = os.path.dirname(file_name)
            logger.error('"{0}" has size zero, aborting.'.format(file_name))
            return

        # strip extension from returned file name (if any) + append file type:
        file_name = os.path.splitext(file_name)[0] + file_type

        file_type_err = False
        fb.fil[1] = fb.fil[0].copy() # backup filter dict
        try:
            with io.open(file_name, 'rb') as f:
                if file_type == '.npz':
                    # http://stackoverflow.com/questions/22661764/storing-a-dict-with-np-savez-gives-unexpected-result

                    # What encoding to use when reading Py2 strings. Only
                    # needed for loading py2 generated pickled files on py3.
                    # fix_imports will try to map old py2 names to new py3
                    # names when unpickling.
                    a = np.load(f, fix_imports=True, encoding='bytes', allow_pickle = True) # array containing dict, dtype 'object'
                    
                    logger.debug("Entries in {0}:\n{1}".format(file_name, a.files))
                    for key in sorted(a):
                        logger.debug("key: {0}|{1}|{2}|{3}".format(key, type(key).__name__, type(a[key]).__name__, a[key]))

                        if np.ndim(a[key]) == 0:
                            # scalar objects may be extracted with the item() method
                            fb.fil[0][key] = a[key].item()
                        else:
                            # array objects are converted to list first
                            fb.fil[0][key] = a[key].tolist()
                elif file_type == '.pkl':
                    # this only works for python >= 3.3
                    fb.fil[0] = pickle.load(f, fix_imports=True, encoding='bytes')
                else:
                    logger.error('Unknown file type "{0}"'.format(file_type))
                    file_type_err = True
                if not file_type_err:
                    # sanitize values in filter dictionary, keys are ok by now
                    for k in fb.fil[0]:
                         # Bytes need to be decoded for py3 to be used as keys later on
                        if type(fb.fil[0][k]) == bytes:
                            fb.fil[0][k] = fb.fil[0][k].decode('utf-8')
                        if fb.fil[0][k] is None:
                            logger.warning("Entry fb.fil[0][{0}] is empty!".format(k))

                    logger.info('Successfully loaded filter\n\t"{0}"'.format(file_name))
                     # emit signal -> InputTabWidgets.load_all:
                    self.sig_tx.emit({"sender":__name__, 'data_changed': 'filter_loaded'})
                    dirs.save_dir = os.path.dirname(file_name) # update working dir
        except IOError as e:
            logger.error("Failed loading {0}!\n{1}".format(file_name, e))
        except Exception as e:
            logger.error("Unexpected error:\n{0}".format(e))
            fb.fil[0] = fb.fil[1] # restore backup
            
#------------------------------------------------------------------------------

def save_filter(self):
    """
    Save filter as zipped binary numpy array or pickle object
    """
    file_filters = ("Zipped Binary Numpy Array (*.npz);;Pickled (*.pkl)")
    dlg = QFD(self)
    # return selected file name (with or without extension) and filter (Linux: full text)
    file_name, file_type = dlg.getSaveFileName_(
            caption = "Save filter as", directory = dirs.save_dir,
            filter = file_filters)

    file_name = str(file_name)  # QString -> str() needed for Python 2.x
    # Qt5 has QFileDialog.mimeTypeFilters(), but under Qt4 the mime type cannot
    # be extracted reproducibly across file systems, so it is done manually:

    for t in extract_file_ext(file_filters): # get a list of file extensions
        if t in str(file_type):
            file_type = t           # return the last matching extension

    if file_name != "": # cancelled file operation returns empty string

        # strip extension from returned file name (if any) + append file type:
        file_name = os.path.splitext(file_name)[0] + file_type

        file_type_err = False
        try:
# =============================================================================
#  # move this part to ellip_zero()
#                 if file_type == '.txt_rpk':
#                     # save as a custom residue/pole text output for apply with custom tool
#                     # make sure we have the residues
#                     if 'rpk' in fb.fil[0]:
#                         with io.open(file_name, 'w', encoding="utf8") as f:
#                             self.file_dump(f)
#                     else:
#                         file_type_err = True
#                         logger.error('Filter has no residues/poles, cannot save as *.txt_rpk file')
#                 else:
# =============================================================================
            with io.open(file_name, 'wb') as f:
                if file_type == '.npz':
                    np.savez(f, **fb.fil[0])
                elif file_type == '.pkl':
                    # save in default pickle version, only compatible with Python 3.x
                    pickle.dump(fb.fil[0], f, protocol = 3)
                else:
                    file_type_err = True
                    logger.error('Unknown file type "{0}"'.format(file_type))

            if not file_type_err:
                logger.info('Successfully saved filter as\n\t"{0}"'.format(file_name))
                dirs.save_dir = os.path.dirname(file_name) # save new dir

        except IOError as e:
            logger.error('Failed saving "{0}"!\n{1}'.format(file_name, e))


#==============================================================================

if __name__=='__main__':
    pass
