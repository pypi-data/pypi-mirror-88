# -*- coding: utf-8 -*-
#
# This file is part of the pyFDA project hosted at https://github.com/chipmuenk/pyfda
#
# Copyright © pyFDA Project Contributors
# Licensed under the terms of the MIT License
# (see file LICENSE in root directory for details)

"""
Design windowed FIR filters (LP, HP, BP, BS) with fixed order, return
the filter design in coefficient ('ba') format

Attention:
This class is re-instantiated dynamically everytime the filter design method
is selected, calling the __init__ method.

API version info:
    1.0: initial working release
    1.1: mark private methods as private
    1.2: new API using fil_save
    1.3: new public methods destruct_UI + construct_UI (no longer called by __init__)
    1.4: module attribute `filter_classes` contains class name and combo box name
         instead of class attribute `name`
         `FRMT` is now a class attribute
    2.0: Specify the parameters for each subwidget as tuples in a dict where the
         first element controls whether the widget is visible and / or enabled.
         This dict is now called self.rt_dict. When present, the dict self.rt_dict_add
         is read and merged with the first one.

    2.1: Remove method destruct_UI and attributes self.wdg and self.hdl

   :2.2: Rename `filter_classes` -> `classes`, remove Py2 compatibility
"""
import logging
logger = logging.getLogger(__name__)

from pyfda.libs.compat import (Qt, QWidget, QLabel, QLineEdit, pyqtSignal, QComboBox, QPushButton,
                      QHBoxLayout, QVBoxLayout)
import numpy as np
import scipy.signal as sig
from scipy.special import sinc

import pyfda.filterbroker as fb # importing filterbroker initializes all its globals
from pyfda.libs.pyfda_lib import fil_save, round_odd, safe_eval, to_html
from pyfda.libs.pyfda_qt_lib import qfilter_warning, qstyle_widget, qget_cmb_box
from pyfda.libs.pyfda_fft_windows_lib import get_window_names, calc_window_function
from pyfda.plot_widgets.plot_fft_win import Plot_FFT_win
from .common import Common, remezord

# TODO: Hilbert, differentiator, multiband are missing
# TODO: Improve calculation of F_C and F_C2 using the weights
# TODO: Automatic setting of density factor for remez calculation?
#       Automatic switching to Kaiser / Hermann?
# TODO: Parameters for windows are not stored in fil_dict?

__version__ = "2.2"

classes = {'Firwin':'Windowed FIR'} #: Dict containing class name : display name

class Firwin(QWidget):

    FRMT = 'ba' # output format(s) of filter design routines 'zpk' / 'ba' / 'sos'
                # currently, only 'ba' is supported for firwin routines

    sig_tx = pyqtSignal(object)

    def __init__(self):
        QWidget.__init__(self)

        self.ft = 'FIR'
        self.fft_window = None
        # dictionary for firwin window settings
        self.win_dict = fb.fil[0]['win_fir']

        c = Common()
        self.rt_dict = c.rt_base_iir

        self.rt_dict_add = {
            'COM':{'min':{'msg':('a',
                                  r"<br /><b>Note:</b> Filter order is only a rough approximation "
                                  "and most likely far too low!")},
                   'man':{'msg':('a',
                                 r"Enter desired filter order <b><i>N</i></b> and "
                                  "<b>-6 dB</b> pass band corner "
                                  "frequency(ies) <b><i>F<sub>C</sub></i></b> .")},
                                  },
            'LP': {'man':{}, 'min':{}},
            'HP': {'man':{'msg':('a', r"<br /><b>Note:</b> Order needs to be odd!")},
                   'min':{}},
            'BS': {'man':{'msg':('a', r"<br /><b>Note:</b> Order needs to be odd!")},
                   'min':{}},
            'BP': {'man':{}, 'min':{}},
            }


        self.info = """**Windowed FIR filters**

        are designed by truncating the
        infinite impulse response of an ideal filter with a window function.
        The kind of used window has strong influence on ripple etc. of the
        resulting filter.

        **Design routines:**

        ``scipy.signal.firwin()``

        """
        #self.info_doc = [] is set in self._update_UI()

        #------------------- end of static info for filter tree ---------------


        #----------------------------------------------------------------------
    def construct_UI(self):
        """
        Create additional subwidget(s) needed for filter design:
        These subwidgets are instantiated dynamically when needed in
        select_filter.py using the handle to the filter object, fb.filObj .
        """

        # Combobox for selecting the algorithm to estimate minimum filter order
        self.cmb_firwin_alg = QComboBox(self)
        self.cmb_firwin_alg.setObjectName('wdg_cmb_firwin_alg')
        self.cmb_firwin_alg.addItems(['ichige','kaiser','herrmann'])
        # Minimum size, can be changed in the upper hierarchy levels using layouts:
        self.cmb_firwin_alg.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.cmb_firwin_alg.hide()

        # Combobox for selecting the window used for filter design
        self.cmb_firwin_win = QComboBox(self)
        self.cmb_firwin_win.addItems(get_window_names())
        self.cmb_firwin_win.setObjectName('wdg_cmb_firwin_win')

        # Minimum size, can be changed in the upper hierarchy levels using layouts:
        self.cmb_firwin_win.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.but_fft_win = QPushButton(self)
        self.but_fft_win.setText("WIN FFT")
        self.but_fft_win.setToolTip("Show time and frequency response of FFT Window")
        self.but_fft_win.setCheckable(True)
        self.but_fft_win.setChecked(False)

        self.lblWinPar1 = QLabel("a", self)
        self.lblWinPar1.setObjectName('wdg_lbl_firwin_1')
        self.ledWinPar1 = QLineEdit(self)
        self.ledWinPar1.setText("0.5")
        self.ledWinPar1.setObjectName('wdg_led_firwin_1')
        self.lblWinPar1.setVisible(False)
        self.ledWinPar1.setVisible(False)

        self.lblWinPar2 = QLabel("b", self)
        self.lblWinPar2.setObjectName('wdg_lbl_firwin_2')
        self.ledWinPar2 = QLineEdit(self)
        self.ledWinPar2.setText("0.5")
        self.ledWinPar2.setObjectName('wdg_led_firwin_2')
        self.ledWinPar2.setVisible(False)
        self.lblWinPar2.setVisible(False)

        self.layHWin1 = QHBoxLayout()
        self.layHWin1.addWidget(self.cmb_firwin_win)
        self.layHWin1.addWidget(self.but_fft_win)
        self.layHWin1.addWidget(self.cmb_firwin_alg)
        self.layHWin2 = QHBoxLayout()
        self.layHWin2.addWidget(self.lblWinPar1)
        self.layHWin2.addWidget(self.ledWinPar1)
        self.layHWin2.addWidget(self.lblWinPar2)
        self.layHWin2.addWidget(self.ledWinPar2)

        self.layVWin = QVBoxLayout()
        self.layVWin.addLayout(self.layHWin1)
        self.layVWin.addLayout(self.layHWin2)
        self.layVWin.setContentsMargins(0,0,0,0)

        # Widget containing all subwidgets (cmbBoxes, Labels, lineEdits)
        self.wdg_fil = QWidget(self)
        self.wdg_fil.setObjectName('wdg_fil')
        self.wdg_fil.setLayout(self.layVWin)

        #----------------------------------------------------------------------
        # SIGNALS & SLOTs
        #----------------------------------------------------------------------
        self.cmb_firwin_alg.activated.connect(self._update_win_fft)
        self.cmb_firwin_win.activated.connect(self._update_win_fft)
        self.ledWinPar1.editingFinished.connect(self._read_param1)
        self.ledWinPar2.editingFinished.connect(self._read_param2)

        self.but_fft_win.clicked.connect(self.show_fft_win)
        #----------------------------------------------------------------------

        self._load_dict() # get initial / last setting from dictionary
        self._update_win_fft()

#=============================================================================
# Copied from impz()
#==============================================================================

    def _read_param1(self):
        """Read out textbox when editing is finished and update dict and fft window"""
        param = safe_eval(self.ledWinPar1.text(), self.win_dict['par'][0]['val'],
                          sign='pos', return_type='float')
        if param < self.win_dict['par'][0]['min']:
            param = self.win_dict['par'][0]['min']
        elif param > self.win_dict['par'][0]['max']:
            param = self.win_dict['par'][0]['max']
        self.ledWinPar1.setText(str(param))
        self.win_dict['par'][0]['val'] = param
        self._update_win_fft()

    def _read_param2(self):
        """Read out textbox when editing is finished and update dict and fft window"""
        param = safe_eval(self.ledWinPar2.text(), self.win_dict['par'][1]['val'],
                          return_type='float')
        if param < self.win_dict['par'][1]['min']:
            param = self.win_dict['par'][1]['min']
        elif param > self.win_dict['par'][1]['max']:
            param = self.win_dict['par'][1]['max']
        self.ledWinPar2.setText(str(param))
        self.win_dict['par'][1]['val'] = param
        self._update_win_fft()

    def _update_win_fft(self):
        """ Update window type for FirWin """
        self.alg = str(self.cmb_firwin_alg.currentText())
        self.fir_window_name = qget_cmb_box(self.cmb_firwin_win, data=False)
        self.win = calc_window_function(self.win_dict, self.fir_window_name,
                                        N=self.N, sym=True)
        n_par = self.win_dict['n_par']

        self.lblWinPar1.setVisible(n_par > 0)
        self.ledWinPar1.setVisible(n_par > 0)
        self.lblWinPar2.setVisible(n_par > 1)
        self.ledWinPar2.setVisible(n_par > 1)

        if n_par > 0:
            self.lblWinPar1.setText(to_html(self.win_dict['par'][0]['name'] + " =", frmt='bi'))
            self.ledWinPar1.setText(str(self.win_dict['par'][0]['val']))
            self.ledWinPar1.setToolTip(self.win_dict['par'][0]['tooltip'])

        if n_par > 1:
            self.lblWinPar2.setText(to_html(self.win_dict['par'][1]['name'] + " =", frmt='bi'))
            self.ledWinPar2.setText(str(self.win_dict['par'][1]['val']))
            self.ledWinPar2.setToolTip(self.win_dict['par'][1]['tooltip'])

        # sig_tx -> select_filter -> filter_specs
        self.sig_tx.emit({'sender':__name__, 'filt_changed':'firwin'})

#=============================================================================

    def _load_dict(self):
        """
        Reload window selection and parameters from filter dictionary
        and set UI elements accordingly. load_dict() is called upon
        initialization and when the filter is loaded from disk.
        """
        self.N = fb.fil[0]['N']
        win_idx = 0
        alg_idx = 0
        if 'wdg_fil' in fb.fil[0] and 'firwin' in fb.fil[0]['wdg_fil']:
            wdg_fil_par = fb.fil[0]['wdg_fil']['firwin']

            if 'win' in wdg_fil_par:
                if np.isscalar(wdg_fil_par['win']): # true for strings (non-vectors)
                    window = wdg_fil_par['win']
                else:
                    window = wdg_fil_par['win'][0]
                    self.ledWinPar1.setText(str(wdg_fil_par['win'][1]))
                    if len(wdg_fil_par['win']) > 2:
                        self.ledWinPar2.setText(str(wdg_fil_par['win'][2]))

                # find index for window string
                win_idx = self.cmb_firwin_win.findText(window,
                                Qt.MatchFixedString) # case insensitive flag
                if win_idx == -1: # Key does not exist, use first entry instead
                    win_idx = 0

            if 'alg' in wdg_fil_par:
                alg_idx = self.cmb_firwin_alg.findText(wdg_fil_par['alg'],
                                Qt.MatchFixedString)
                if alg_idx == -1: # Key does not exist, use first entry instead
                    alg_idx = 0

        self.cmb_firwin_win.setCurrentIndex(win_idx) # set index for window and
        self.cmb_firwin_alg.setCurrentIndex(alg_idx) # and algorithm cmbBox

    def _store_entries(self):
        """
        Store window and alg. selection and parameter settings (part of
        self.firWindow, if any) in filter dictionary.
        """
        if not 'wdg_fil' in fb.fil[0]:
            fb.fil[0].update({'wdg_fil':{}})
        fb.fil[0]['wdg_fil'].update({'firwin':
                                        {'win':self.firWindow,
                                         'alg':self.alg}
                                 })


    def _get_params(self, fil_dict):
        """
        Translate parameters from the passed dictionary to instance
        parameters, scaling / transforming them if needed.
        """
        self.N     = fil_dict['N']
        self.F_PB  = fil_dict['F_PB']
        self.F_SB  = fil_dict['F_SB']
        self.F_PB2 = fil_dict['F_PB2']
        self.F_SB2 = fil_dict['F_SB2']
        self.F_C   = fil_dict['F_C']
        self.F_C2  = fil_dict['F_C2']

        # firwin amplitude specs are linear (not in dBs)
        self.A_PB  = fil_dict['A_PB']
        self.A_PB2 = fil_dict['A_PB2']
        self.A_SB  = fil_dict['A_SB']
        self.A_SB2 = fil_dict['A_SB2']

#        self.alg = 'ichige' # algorithm for determining the minimum order
#        self.alg = self.cmb_firwin_alg.currentText()

    def _test_N(self):
        """
        Warn the user if the calculated order is too high for a reasonable filter
        design.
        """
        if self.N > 1000:
            return qfilter_warning(self, self.N, "FirWin")
        else:
            return True


    def _save(self, fil_dict, arg):
        """
        Convert between poles / zeros / gain, filter coefficients (polynomes)
        and second-order sections and store all available formats in the passed
        dictionary 'fil_dict'.
        """
        fil_save(fil_dict, arg, self.FRMT, __name__)

        try: # has the order been calculated by a "min" filter design?
            fil_dict['N'] = self.N # yes, update filterbroker
        except AttributeError:
            pass
#        self._store_entries()

#------------------------------------------------------------------------------
    def firwin(self, numtaps, cutoff, window=None, pass_zero=True,
               scale=True, nyq=1.0, fs=None):

        """
        FIR filter design using the window method. This is more or less the
        same as `scipy.signal.firwin` with the exception that an ndarray with
        the window values can be passed as an alternative to the window name.

        The parameters "width" (specifying a Kaiser window) and "fs" have been
        omitted, they are not needed here.

        This function computes the coefficients of a finite impulse response
        filter.  The filter will have linear phase; it will be Type I if
        `numtaps` is odd and Type II if `numtaps` is even.
        Type II filters always have zero response at the Nyquist rate, so a
        ValueError exception is raised if firwin is called with `numtaps` even and
        having a passband whose right end is at the Nyquist rate.

        Parameters
        ----------
        numtaps : int
            Length of the filter (number of coefficients, i.e. the filter
            order + 1).  `numtaps` must be even if a passband includes the
            Nyquist frequency.
        cutoff : float or 1D array_like
            Cutoff frequency of filter (expressed in the same units as `nyq`)
            OR an array of cutoff frequencies (that is, band edges). In the
            latter case, the frequencies in `cutoff` should be positive and
            monotonically increasing between 0 and `nyq`.  The values 0 and
            `nyq` must not be included in `cutoff`.
        window : ndarray or string
            string: use the window with the passed name from scipy.signal.windows

            ndarray: The window values - this is an addition to the original
            firwin routine.
        pass_zero : bool, optional
            If True, the gain at the frequency 0 (i.e. the "DC gain") is 1.
            Otherwise the DC gain is 0.
        scale : bool, optional
            Set to True to scale the coefficients so that the frequency
            response is exactly unity at a certain frequency.
            That frequency is either:
            - 0 (DC) if the first passband starts at 0 (i.e. pass_zero
              is True)
            - `nyq` (the Nyquist rate) if the first passband ends at
              `nyq` (i.e the filter is a single band highpass filter);
              center of first passband otherwise
        nyq : float, optional
            Nyquist frequency.  Each frequency in `cutoff` must be between 0
            and `nyq`.
        Returns
        -------
        h : (numtaps,) ndarray
            Coefficients of length `numtaps` FIR filter.
        Raises
        ------
        ValueError
            If any value in `cutoff` is less than or equal to 0 or greater
            than or equal to `nyq`, if the values in `cutoff` are not strictly
            monotonically increasing, or if `numtaps` is even but a passband
            includes the Nyquist frequency.
        See also
        --------
        scipy.firwin
        """
        cutoff = np.atleast_1d(cutoff) / float(nyq)

        # Check for invalid input.
        if cutoff.ndim > 1:
            raise ValueError("The cutoff argument must be at most "
                             "one-dimensional.")
        if cutoff.size == 0:
            raise ValueError("At least one cutoff frequency must be given.")
        if cutoff.min() <= 0 or cutoff.max() >= 1:
            raise ValueError("Invalid cutoff frequency {0}: frequencies must be "
                             "greater than 0 and less than nyq.".format(cutoff))
        if np.any(np.diff(cutoff) <= 0):
            raise ValueError("Invalid cutoff frequencies: the frequencies "
                             "must be strictly increasing.")

        pass_nyquist = bool(cutoff.size & 1) ^ pass_zero
        if pass_nyquist and numtaps % 2 == 0:
            raise ValueError("A filter with an even number of coefficients must "
                             "have zero response at the Nyquist rate.")

        # Insert 0 and/or 1 at the ends of cutoff so that the length of cutoff
        # is even, and each pair in cutoff corresponds to passband.
        cutoff = np.hstack(([0.0] * pass_zero, cutoff, [1.0] * pass_nyquist))

        # `bands` is a 2D array; each row gives the left and right edges of
        # a passband.
        bands = cutoff.reshape(-1, 2)

        # Build up the coefficients.
        alpha = 0.5 * (numtaps - 1)
        m = np.arange(0, numtaps) - alpha
        h = 0
        for left, right in bands:
            h += right * sinc(right * m)
            h -= left * sinc(left * m)

        if type(window) == str:
            # Get and apply the window function.
            from scipy.signal.signaltools import get_window
            win = get_window(window, numtaps, fftbins=False)
        elif type(window) == np.ndarray:
            win = window
        else:
            logger.error("The 'window' was neither a string nor a numpy array, it could not be evaluated.")
            return None
        # apply the window function.
        h *= win

        # Now handle scaling if desired.
        if scale:
            # Get the first passband.
            left, right = bands[0]
            if left == 0:
                scale_frequency = 0.0
            elif right == 1:
                scale_frequency = 1.0
            else:
                scale_frequency = 0.5 * (left + right)
            c = np.cos(np.pi * m * scale_frequency)
            s = np.sum(h * c)
            h /= s

        return h


    def _firwin_ord(self, F, W, A, alg):
        #http://www.mikroe.com/chapters/view/72/chapter-2-fir-filters/
        delta_f = abs(F[1] - F[0]) * 2 # referred to f_Ny
        delta_A = np.sqrt(A[0] * A[1])
        if self.fir_window_name == 'kaiser':
            N, beta = sig.kaiserord(20 * np.log10(np.abs(fb.fil[0]['A_SB'])), delta_f)
            self.ledWinPar1.setText(str(beta))
            fb.fil[0]['wdg_fil'][1] = beta
            self._update_UI()
        else:
            N = remezord(F, W, A, fs = 1, alg = alg)[0]

        return N

    def LPmin(self, fil_dict):
        self._get_params(fil_dict)
        self.N = self._firwin_ord([self.F_PB, self.F_SB], [1, 0],
                                 [self.A_PB, self.A_SB], alg = self.alg)
        if not self._test_N():
            return -1
        self.fir_window = calc_window_function(self.win_dict, self.fir_window_name,
                                        N=self.N, sym=True)
        fil_dict['F_C'] = (self.F_SB + self.F_PB)/2 # use average of calculated F_PB and F_SB
        self._save(fil_dict, self.firwin(self.N, fil_dict['F_C'],
                                       window = self.fir_window, nyq = 0.5))

    def LPman(self, fil_dict):
        self._get_params(fil_dict)
        if not self._test_N():
            return -1
        self.fir_window = calc_window_function(self.win_dict, self.fir_window_name,
                                        N=self.N, sym=True)
        self._save(fil_dict, self.firwin(self.N, fil_dict['F_C'],
                                       window = self.fir_window, nyq = 0.5))

    def HPmin(self, fil_dict):
        self._get_params(fil_dict)
        N = self._firwin_ord([self.F_SB, self.F_PB], [0, 1],
                            [self.A_SB, self.A_PB], alg = self.alg)
        self.N = round_odd(N)  # enforce odd order
        if not self._test_N():
            return -1
        self.fir_window = calc_window_function(self.win_dict, self.fir_window_name,
                                        N=self.N, sym=True)
        fil_dict['F_C'] = (self.F_SB + self.F_PB)/2 # use average of calculated F_PB and F_SB
        self._save(fil_dict, self.firwin(self.N, fil_dict['F_C'],
                    window = self.fir_window, pass_zero=False, nyq = 0.5))

    def HPman(self, fil_dict):
        self._get_params(fil_dict)
        self.N = round_odd(self.N)  # enforce odd order
        if not self._test_N():
            return -1
        self.fir_window = calc_window_function(self.win_dict, self.fir_window_name,
                                        N=self.N, sym=True)
        self._save(fil_dict, self.firwin(self.N, fil_dict['F_C'],
            window = self.fir_window, pass_zero=False, nyq = 0.5))

    # For BP and BS, F_PB and F_SB have two elements each
    def BPmin(self, fil_dict):
        self._get_params(fil_dict)
        self.N = remezord([self.F_SB, self.F_PB, self.F_PB2, self.F_SB2], [0, 1, 0],
            [self.A_SB, self.A_PB, self.A_SB2], fs = 1, alg = self.alg)[0]
        if not self._test_N():
            return -1
        self.fir_window = calc_window_function(self.win_dict, self.fir_window_name,
                                        N=self.N, sym=True)

        fil_dict['F_C'] = (self.F_SB + self.F_PB)/2 # use average of calculated F_PB and F_SB
        fil_dict['F_C2'] = (self.F_SB2 + self.F_PB2)/2 # use average of calculated F_PB and F_SB
        self._save(fil_dict, self.firwin(self.N, [fil_dict['F_C'], fil_dict['F_C2']],
                            window = self.fir_window, pass_zero=False, nyq = 0.5))

    def BPman(self, fil_dict):
        self._get_params(fil_dict)
        if not self._test_N():
            return -1
        self.fir_window = calc_window_function(self.win_dict, self.fir_window_name,
                                        N=self.N, sym=True)
        self._save(fil_dict, self.firwin(self.N, [fil_dict['F_C'], fil_dict['F_C2']],
                            window = self.fir_window, pass_zero=False, nyq = 0.5))

    def BSmin(self, fil_dict):
        self._get_params(fil_dict)
        N = remezord([self.F_PB, self.F_SB, self.F_SB2, self.F_PB2], [1, 0, 1],
            [self.A_PB, self.A_SB, self.A_PB2], fs = 1, alg = self.alg)[0]
        self.N = round_odd(N)  # enforce odd order
        if not self._test_N():
            return -1
        self.fir_window = calc_window_function(self.win_dict, self.fir_window_name,
                                        N=self.N, sym=True)
        fil_dict['F_C'] = (self.F_SB + self.F_PB)/2 # use average of calculated F_PB and F_SB
        fil_dict['F_C2'] = (self.F_SB2 + self.F_PB2)/2 # use average of calculated F_PB and F_SB
        self._save(fil_dict, self.firwin(self.N, [fil_dict['F_C'], fil_dict['F_C2']],
                            window = self.fir_window, pass_zero=True, nyq = 0.5))

    def BSman(self, fil_dict):
        self._get_params(fil_dict)
        self.N = round_odd(self.N)  # enforce odd order
        if not self._test_N():
            return -1
        self.fir_window = calc_window_function(self.win_dict, self.fir_window_name,
                                        N=self.N, sym=True)
        self._save(fil_dict, self.firwin(self.N, [fil_dict['F_C'], fil_dict['F_C2']],
                            window = self.fir_window, pass_zero=True, nyq = 0.5))

    #------------------------------------------------------------------------------
    def show_fft_win(self):
        """
        Pop-up FFT window
        """
        if self.but_fft_win.isChecked():
            qstyle_widget(self.but_fft_win, "changed")
        else:
            qstyle_widget(self.but_fft_win, "normal")

        if self.fft_window is None: # no handle to the window? Create a new instance
            if self.but_fft_win.isChecked():
                # important: Handle to window must be class attribute
                # pass the name of the dictionary where parameters are stored and
                # whether a symmetric window or one that can be continued periodically
                # will be constructed
                self.fft_window = Plot_FFT_win(self, win_dict=self.win_dict, sym=True,
                                               title="pyFDA FIR Window Viewer")
                self.sig_tx.connect(self.fft_window.sig_rx)
                self.fft_window.sig_tx.connect(self.close_fft_win)
                self.fft_window.show() # modeless i.e. non-blocking popup window
        else:
            if not self.but_fft_win.isChecked():
                if self.fft_window is None:
                    logger.warning("FFT window is already closed!")
                else:
                    self.fft_window.close()

    def close_fft_win(self):
        self.fft_window = None
        self.but_fft_win.setChecked(False)
        qstyle_widget(self.but_fft_win, "normal")

#------------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    from pyfda.libs.compat import QApplication, QFrame

    app = QApplication(sys.argv)

    # instantiate filter widget
    filt = Firwin()
    filt.construct_UI()
    wdg_firwin = getattr(filt, 'wdg_fil')

    layVDynWdg = QVBoxLayout()
    layVDynWdg.addWidget(wdg_firwin, stretch = 1)

    filt.LPman(fb.fil[0])  # design a low-pass with parameters from global dict
    print(fb.fil[0][filt.FRMT]) # return results in default format

    frmMain = QFrame()
    frmMain.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
    frmMain.setLayout(layVDynWdg)

    form = frmMain

    form.show()

    app.exec_()

# test using "python -m pyfda.filter_designs.firwin"

