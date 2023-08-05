# -*- coding: utf-8 -*-
#
# This file is part of the pyFDA project hosted at https://github.com/chipmuenk/pyfda
#
# Copyright © pyFDA Project Contributors
# Licensed under the terms of the MIT License
# (see file LICENSE in root directory for details)

"""
Helper classes and functions for generating and simulating fixpoint filters
"""
import sys
import logging
logger = logging.getLogger(__name__)
#import numpy as np
import pyfda.filterbroker as fb
import pyfda.libs.pyfda_fix_lib as fx

from pyfda.libs.compat import (QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QIcon,
                      QVBoxLayout, QHBoxLayout, QFrame,
                      pyqtSignal)

from migen import Cat, If, Replicate, Signal

from pyfda.libs.pyfda_qt_lib import qget_cmb_box, qset_cmb_box
from pyfda.pyfda_rc import params
from pyfda.libs.pyfda_lib import qstr, safe_eval, to_html


def requant(mod, sig_i, QI, QO):
    """
    Change word length of input signal `sig_i` to `WO` bits, using the 
    quantization and saturation methods specified by ``QO['quant']`` and 
    ``QO['ovfl']``.
    
    Parameters
    ----------
    
    mod: Module (migen)
        instance of migen module
    
    sig_i: Signal (migen)
        Signal to be requantized
    
    QI: dict
        Quantization dict for input word, only the keys 'WI' and 'WF' for integer
        and fractional wordlength are evaluated. QI['WI'] = 2 and QI['WF'] = 13
        e.g. define Q-Format '2.13'  with 2 integer, 13 fractional bits and 1 implied 
        sign bit = 16 bits total.
    
    QO: dict
        Quantization dict for output word format; the keys 'WI' and 'WF' for 
        integer and fractional wordlength are evaluated as well as the keys 'quant'
        and 'ovfl' describing requantization and overflow behaviour.

    Returns
    -------

    sig_o: Signal (migen)
        Requantized signal

    Documentation
    -------------

    **Input and output word are aligned at their binary points.**
    
    The following shows an example of rescaling an input word from Q2.4 to Q0.3
    using wrap-around and truncation. It's easy to see that for simple wrap-around
    logic, the sign of the result may change.
    
    ::

      S | WI1 | WI0 * WF0 | WF1 | WF2 | WF3  :  WI = 2, WF = 4, W = 7
      0 |  1  |  0  *  1  |  0  |  1  |  1   =  43 (dec) or 43/16 = 2 + 11/16 (float)
                    *
              |  S  * WF0 | WF1 | WF2        :  WI = 0, WF = 3, W = 4
                 0  *  1  |  0  |  1         =  7 (dec) or 7/8 (float)

              
    The float or "real (world) value" is calculated by multiplying the integer 
    value by 2 ** (-WF).
    
    For requantizing two numbers to the same WI and WF, imagine both binary numbers
    to be right-aligned. Changes in the number of integer bits `dWI` and fractional
    bits `dWF` are handled separately.
    
    Fractional Bits
    ---------------
    
    - For reducing the number of fractional bits by `dWF`, simply right-shift the
      integer number by `dWF`. For rounding, add '1' to the bit below the truncation
      point before right-shifting. 
    
    - Extend the number of fractional bits by left-shifting the integer by `dWF`,
      LSB's are filled with zeros.
      
    Integer Bits
    ------------
    
    - For reducing the number of integer bits by `dWI`, simply right-shift the
      integer by `dWI`.
    
    - The number of fractional bits is SIGN-EXTENDED by filling up the left-most
      bits with the sign bit.
    
    """
    WI_I = QI['WI']         # number of integer bits (input signal)
    WI_F = QI['WF']         # number of integer bits (output signal)
    WI   = WI_I + WI_F + 1  # total word length (input signal)

    WO_I = QO['WI']         # number of integer bits (input signal)
    WO_F = QO['WF']         # number of integer bits (output signal)
    WO   = WO_I + WO_F + 1  # total word length (input signal)

    dWF = WI_F - WO_F       # difference of fractional lengths
    dWI = WI_I - WO_I       # difference of integer lengths

    # max. resp. min, output values
    MIN_o = - 1 << (WO - 1)
    MAX_o = -MIN_o - 1

    sig_i_q = Signal((max(WI,WO), True)) # intermediate signal with requantized fractional part
    sig_o = Signal((WO, True))

    logger.debug("rescale: dWI={0}, dWF={1}, QU:{2}, OV:{3}".format(dWI, dWF, QO['quant'], QO['ovfl'] ))
    if dWF <= 0: # Extend fractional word length of output word by multiplying with 2^dWF 
        mod.comb += sig_i_q.eq(sig_i << -dWF) #  shift input left by -dWF   
    else: # dWF > 0, reduce fractional word length by dividing by 2^dWF (shift right by dWF)
        if QO['quant'] == 'round':
            # add half an LSB (1 << (dWF - 1)) before right shift 
            mod.comb += sig_i_q.eq((sig_i + (1 << (dWF - 1))) >> dWF)
        elif QO['quant'] == 'floor': # just shift right
            mod.comb += sig_i_q.eq(sig_i >> dWF)
        elif QO['quant'] == 'fix':
            # add sign bit (sig_i[-1]) as LSB (1 << dWF) before right shift
            mod.comb += sig_i_q.eq((sig_i + (sig_i[-1] << dWF)) >> dWF)
        else:
            raise Exception(u'Unknown quantization method "%s"!'%(QI['quant']))
 
    # -----------------------------------------------------------------------
    # Requantize integer part 
    # -----------------------------------------------------------------------
    if dWI < 0: # WI_I < WO_I, sign extend integer part (prepend copies of sign bit)
        mod.comb += sig_o.eq(Cat(sig_i_q, Replicate(sig_i_q[-1], -dWI)))
    elif dWI == 0: # WI = WO, don't change integer part
        mod.comb += sig_o.eq(sig_i_q)
    elif QO['ovfl'] == 'sat':
        mod.comb += \
            If(sig_i_q[-1] == 1,
               If(sig_i_q < MIN_o,
                    sig_o.eq(MIN_o)
                ).Else(sig_o.eq(sig_i_q))
            ).Elif(sig_i_q > MAX_o,
                sig_o.eq(MAX_o)
            ).Else(sig_o.eq(sig_i_q)
            )
    elif QO['ovfl'] == 'wrap': # wrap around (shift left)
        mod.comb += sig_o.eq(sig_i_q)

# =============================================================================
#             If(sig_i_q[-1] == 1,
#                If(sig_i_q[-1:-dWI-1] != Replicate(sig_i_q[-1], dWI),
#             #If(sig_i_q < MIN_o,
#             #If(sig_i_q[WO-1:] == 0b10,
#                     sig_o.eq(MIN_o)
#                 ).Else(sig_o.eq(sig_i_q)# >> dWI
#             ).Elif(sig_i_q > MAX_o,
#             #).Elif(sig_i_q[WO-1:] == 0b01,
#                 sig_o.eq(MAX_o)
#             ).Else(sig_o.eq(sig_i_q)# >> dWI)
#             )
# =============================================================================

    else:
        raise Exception(u'Unknown overflow method "%s"!'%(QI['ovfl']))

    return sig_o

#------------------------------------------------------------------------------
class UI_W(QWidget):
    """
    Widget for entering integer and fractional bits. The result can be read out
    via the attributes `self.WI`, `self.WF` and `self.W`.
    
    The constructor accepts a dictionary for initial widget settings.
    The following keys are defined; default values are used for missing keys:

    'id'            : 'ui_w'                    # widget id
    'label'         : 'WI.WF'                   # widget text label
    'visible'       : True                      # Is widget visible?
    'enabled'       : True                      # Is widget enabled?

    'fractional'    : True                      # Display WF, otherwise WF=0
    'lbl_sep'       : '.'                       # label between WI and WF field
    'max_led_width' : 30                        # max. length of lineedit field
    'WI'            : 0                         # number of frac. *bits*                
    'WI_len'        : 2                         # max. number of integer *digits*
    'tip_WI'        : 'Number of integer bits'  # Mouse-over tooltip
    'WF'            : 15                        # number of frac. *bits*
    'WF_len'        : 2                         # max. number of frac. *digits*
    'tip_WF'        : 'Number of frac. bits'    # Mouse-over tooltip

    
    'lock_visible'  : False                     # Pushbutton for locking visible
    'tip_lock'      : 'Lock input/output quant.'# Tooltip for  lock push button
    
    'combo_visible' : False                     # Enable integrated combo widget
    'combo_items'   : ['auto', 'full', 'man']   # Combo selection
    'tip_combo'     : 'Calculate Acc. width.'   # tooltip for combo
    """
    # incoming, 
    #sig_rx = pyqtSignal(object)
    # outcgoing
    sig_tx = pyqtSignal(object)

    def __init__(self, parent, q_dict, **kwargs):
        super(UI_W, self).__init__(parent)
        self.q_dict = q_dict # pass a dict with initial settings for construction
        self._construct_UI(**kwargs)
        self.ui2dict(s='init') # initialize the class attributes

    def _construct_UI(self, **kwargs):
        """ 
        Construct widget from quantization dict, individual settings and
        the default dict below """

        # default settings
        dict_ui = {'id':'ui_w', 'label':'WI.WF', 'lbl_sep':'.', 'max_led_width':30,
                   'WI':0, 'WI_len':2, 'tip_WI':'Number of integer bits',
                   'WF':15,'WF_len':2, 'tip_WF':'Number of fractional bits',
                   'enabled':True, 'visible':True, 'fractional':True,
                   'combo_visible':False, 'combo_items':['auto', 'full', 'man'],
                   'tip_combo':'Calculate Acc. width.',                  
                   'lock_visible':False, 'tip_lock':'Lock input/output quantization.'
                   } #: default values

        if self.q_dict:
            dict_ui.update(self.q_dict)
            
        for k, v in kwargs.items():
            if k not in dict_ui:
                logger.warning("Unknown key {0}".format(k))
            else:
                dict_ui.update({k:v})

        self.id = dict_ui['id']

        if not dict_ui['fractional']:
            dict_ui['WF'] = 0
        self.WI = dict_ui['WI']
        self.WF = dict_ui['WF']
        self.W = int(self.WI + self.WF + 1)
        if self.q_dict:
            self.q_dict.update({'WI':self.WI, 'WF':self.WF, 'W':self.W})
        else:
            self.q_dict = {'WI':self.WI, 'WF':self.WF, 'W':self.W}

        lblW = QLabel(to_html(dict_ui['label'], frmt='bi'), self)

        self.cmbW = QComboBox(self)
        self.cmbW.addItems(dict_ui['combo_items'])
        self.cmbW.setVisible(dict_ui['combo_visible'])
        self.cmbW.setToolTip(dict_ui['tip_combo'])
        self.cmbW.setObjectName("cmbW")
        
        self.butLock = QPushButton(self)
        self.butLock.setCheckable(True)
        self.butLock.setChecked(False)
        self.butLock.setVisible(dict_ui['lock_visible'])
        self.butLock.setToolTip(dict_ui['tip_lock'])

        self.ledWI = QLineEdit(self)
        self.ledWI.setToolTip(dict_ui['tip_WI'])
        self.ledWI.setMaxLength(dict_ui['WI_len']) # maximum of 2 digits
        self.ledWI.setFixedWidth(dict_ui['max_led_width']) # width of lineedit in points(?)
        self.ledWI.setObjectName("WI")

        lblDot = QLabel(dict_ui['lbl_sep'], self)
        lblDot.setVisible(dict_ui['fractional'])

        self.ledWF = QLineEdit(self)
        self.ledWF.setToolTip(dict_ui['tip_WF'])
        self.ledWF.setMaxLength(dict_ui['WI_len']) # maximum of 2 digits
        self.ledWF.setFixedWidth(dict_ui['max_led_width']) # width of lineedit in points(?)
        self.ledWF.setVisible(dict_ui['fractional'])
        self.ledWF.setObjectName("WF")
        
        layH = QHBoxLayout()
        layH.addWidget(lblW)
        layH.addStretch()
        layH.addWidget(self.cmbW)
        layH.addWidget(self.butLock)
        layH.addWidget(self.ledWI)
        layH.addWidget(lblDot)
        layH.addWidget(self.ledWF)
        layH.setContentsMargins(0,0,0,0)

        frmMain = QFrame(self)
        frmMain.setLayout(layH)

        layVMain = QVBoxLayout() # Widget main layout
        layVMain.addWidget(frmMain)
        layVMain.setContentsMargins(0,5,0,0)#*params['wdg_margins'])

        self.setLayout(layVMain)
        
        #----------------------------------------------------------------------
        # INITIAL SETTINGS
        #----------------------------------------------------------------------
        self.ledWI.setText(qstr(dict_ui['WI']))
        self.ledWF.setText(qstr(dict_ui['WF']))

        frmMain.setEnabled(dict_ui['enabled'])
        frmMain.setVisible(dict_ui['visible'])

        #----------------------------------------------------------------------
        # LOCAL SIGNALS & SLOTs
        #----------------------------------------------------------------------
        self.ledWI.editingFinished.connect(self.ui2dict)
        self.ledWF.editingFinished.connect(self.ui2dict)
        self.butLock.clicked.connect(self.butLock_clicked)
        self.cmbW.currentIndexChanged.connect(self.ui2dict)

        # initialize button icon        
        self.butLock_clicked(self.butLock.isChecked())

    def quant_coeffs(self, q_dict, coeffs):
        """
        Quantize the coefficients, scale and convert them to integer and return them
        as a list of integers
        
        This is called every time one of the coefficient subwidgets is edited or changed.
    
        Parameters:
        -----------
        None
    
        Returns:
        --------
        A list of integer coeffcients, quantized and scaled with the settings
        of the passed quantization dict
               
        """
        # Create coefficient quantizer instances using the quantization parameters dict
        # collected in `input_widgets/input_coeffs.py` (and stored in the central filter dict)
        Q_coeff = fx.Fixed(q_dict)
        Q_coeff.frmt = 'dec' # always use decimal format for coefficients

        if coeffs is None:
            logger.error("Coeffs empty!")
        # quantize floating point coefficients and convert them to the
        # selected numeric format (hex, bin, dec ...) with the selected scale (WI.WF),
        # next convert array float -> array of fixp - > list of int (scaled by 2^WF)
        return list(Q_coeff.float2frmt(coeffs) * (1 << Q_coeff.WF))

    #--------------------------------------------------------------------------
    def butLock_clicked(self, clicked):
        """ 
        Update the icon of the push button depending on its state
        """
        if clicked:
            self.butLock.setIcon(QIcon(':/lock-locked.svg'))
        else:
            self.butLock.setIcon(QIcon(':/lock-unlocked.svg'))
            
        q_icon_size = self.butLock.iconSize() # <- uncomment this for manual sizing
        self.butLock.setIconSize(q_icon_size)

        dict_sig = {'sender':__name__, 'id':self.id, 'ui':'butLock'}
        self.sig_tx.emit(dict_sig)
        
    #--------------------------------------------------------------------------
    def ui2dict(self, s=None):
        """ 
        Update the attributes `self.WI`, `self.WF` and `self.W` and `self.q_dict`
        when one of the QLineEdit widgets has been edited.
        
        Emit a signal with `{'ui':objectName of the sender}`.
        """

        self.WI = int(safe_eval(self.ledWI.text(), self.WI, return_type="int", sign='poszero'))
        self.ledWI.setText(qstr(self.WI))
        self.WF = int(safe_eval(self.ledWF.text(), self.WF, return_type="int", sign='poszero'))
        self.ledWF.setText(qstr(self.WF))
        self.W = int(self.WI + self.WF + 1)

        self.q_dict.update({'WI':self.WI, 'WF':self.WF, 'W':self.W})

        if self.sender():
            name = self.sender().objectName()
            logger.debug("sender: {0}".format(name))
            dict_sig = {'sender':__name__, 'id':self.id, 'ui':name}
            self.sig_tx.emit(dict_sig)
        elif s=='init':
            logger.debug("called by __init__")
        else:
            logger.error("sender without name!")
            
        
    #--------------------------------------------------------------------------
    def dict2ui(self, q_dict=None):
        """ 
        Update the widgets `WI` and `WF` and the corresponding attributes
        from the dict passed as the argument
        """
        if q_dict is None:
            q_dict = self.q_dict
            
        if 'WI' in q_dict:
            self.WI = safe_eval(q_dict['WI'], self.WI, return_type="int", sign='poszero')
            self.ledWI.setText(qstr(self.WI))
        else:
            logger.warning("No key 'WI' in dict!")

        if 'WF' in q_dict:
            self.WF = safe_eval(q_dict['WF'], self.WF, return_type="int", sign='poszero')
            self.ledWF.setText(qstr(self.WF))
        else:
            logger.warning("No key 'WF' in dict!")
        
        self.W = self.WF + self.WI + 1

#------------------------------------------------------------------------------
#        
#==============================================================================
class UI_Q(QWidget):
    """
    Widget for selecting quantization / overflow options. The result can be read out
    via the attributes `self.ovfl` and `self.quant`.
    
    The constructor accepts a reference to the quantization dictionary for
    initial widget settings and for (re-)storing values.
    
    The following keys are defined; default values are used for missing keys:

    'id'        : 'ui_q'                            # widget id
    'label'     : ''                                # widget text label
    
    'label_q'   : 'Quant.'                          # subwidget text label
    'tip_q'     : 'Select kind of quantization.'    # Mouse-over tooltip
    'cmb_q'     : [round', 'fix', 'floor']          # combo-box choices
    'cur_q'     : 'round'                           # initial / current setting
 
    'label_ov'  : 'Ovfl.'                           # subwidget text label
    'tip_ov'    : 'Select overflow behaviour.'      # Mouse-over tooltip
    'cmb_ov'    : ['wrap', 'sat']                   # combo-box choices
    'cur_ov'    : 'wrap'                            # initial / current setting

    'enabled'   : True                              # Is widget enabled?
    'visible'   : True                              # Is widget visible?
    """
    # incoming, 
    #sig_rx = pyqtSignal(object)
    # outcgoing
    sig_tx = pyqtSignal(object)

    def __init__(self, parent, q_dict, **kwargs):
        super(UI_Q, self).__init__(parent)
        self.q_dict = q_dict
        self._construct_UI(**kwargs)

    def _construct_UI(self, **kwargs):
        """ Construct widget """

        dict_ui = {'id':'ui_q', 'label':'',
                   'label_q':'Quant.', 'tip_q':'Select the kind of quantization.',
                   'cmb_q':['round', 'fix', 'floor'], 'cur_q':'round',
                   'label_ov':'Ovfl.', 'tip_ov':'Select overflow behaviour.',
                   'cmb_ov':['wrap', 'sat'], 'cur_ov':'wrap',
                   'enabled':True, 'visible':True
                   } #: default widget settings

        if 'quant' in self.q_dict and self.q_dict['quant'] in dict_ui['cmb_q']:
            dict_ui['cur_q'] = self.q_dict['quant']
        if 'ovfl' in self.q_dict and self.q_dict['ovfl'] in dict_ui['cmb_ov']:
            dict_ui['cur_ov'] = self.q_dict['ovfl']
            
        for key, val in kwargs.items():
            dict_ui.update({key:val})
        # dict_ui.update(map(kwargs)) # same as above?
            
        self.id = dict_ui['id']
        
        lblQuant = QLabel(dict_ui['label_q'], self)
        self.cmbQuant = QComboBox(self)
        self.cmbQuant.addItems(dict_ui['cmb_q'])
        qset_cmb_box(self.cmbQuant, dict_ui['cur_q'])
        self.cmbQuant.setToolTip(dict_ui['tip_q'])
        self.cmbQuant.setObjectName('quant')        

        lblOvfl = QLabel(dict_ui['label_ov'], self)
        self.cmbOvfl = QComboBox(self)
        self.cmbOvfl.addItems(dict_ui['cmb_ov'])
        qset_cmb_box(self.cmbOvfl, dict_ui['cur_ov'])
        self.cmbOvfl.setToolTip(dict_ui['tip_ov'])
        self.cmbOvfl.setObjectName('ovfl')
        
        # ComboBox size is adjusted automatically to fit the longest element
        self.cmbQuant.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.cmbOvfl.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        layH = QHBoxLayout()
        if dict_ui['label'] != "":
            lblW = QLabel(to_html(dict_ui['label'], frmt='bi'), self)
            layH.addWidget(lblW)
        layH.addStretch()
        layH.addWidget(lblOvfl)
        layH.addWidget(self.cmbOvfl)
        #layH.addStretch(1)
        layH.addWidget(lblQuant)
        layH.addWidget(self.cmbQuant)
        layH.setContentsMargins(0,0,0,0)

        frmMain = QFrame(self)
        frmMain.setLayout(layH)

        layVMain = QVBoxLayout() # Widget main layout
        layVMain.addWidget(frmMain)
        layVMain.setContentsMargins(0,0,0,0)#*params['wdg_margins'])

        self.setLayout(layVMain)

        #----------------------------------------------------------------------
        # INITIAL SETTINGS
        #----------------------------------------------------------------------
        self.ovfl = qget_cmb_box(self.cmbOvfl, data=False)
        self.quant = qget_cmb_box(self.cmbQuant, data=False)
        
        frmMain.setEnabled(dict_ui['enabled'])
        frmMain.setVisible(dict_ui['visible'])

        #----------------------------------------------------------------------
        # LOCAL SIGNALS & SLOTs
        #----------------------------------------------------------------------
        self.cmbOvfl.currentIndexChanged.connect(self.ui2dict)
        self.cmbQuant.currentIndexChanged.connect(self.ui2dict)

    #--------------------------------------------------------------------------
    def ui2dict(self):
        """ 
        Update the quantization dict and the attributes `self.ovfl` and 
        `self.quant` from the UI
        """
        self.ovfl = self.cmbOvfl.currentText()
        self.quant = self.cmbQuant.currentText()
        
        self.q_dict.update({'ovfl': self.ovfl,
                            'quant': self.quant})
        
        if self.sender():
            name = self.sender().objectName()
            dict_sig = {'sender':__name__, 'id':self.id, 'ui':name}
            self.sig_tx.emit(dict_sig)

    #--------------------------------------------------------------------------
    def dict2ui(self, q_dict):
        """ Update UI from passed dictionary """
        pass

#==============================================================================

if __name__ == '__main__':

    from pyfda.libs.compat import QApplication
    app = QApplication(sys.argv)
    mainw = UI_W(None)
    mainw.show()

    app.exec_()