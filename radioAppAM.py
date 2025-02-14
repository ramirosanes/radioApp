#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: radioAppAM
# Author: rami
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from datetime import datetime
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
import os
import osmosdr
import time
import sip



class radioAppAM(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "radioAppAM", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("radioAppAM")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "radioAppAM")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.offset = offset = 125e6
        self.station2 = station2 = 580e3
        self.station1 = station1 = 580e3
        self.samp_rate = samp_rate = 2560000
        self.rootdir = rootdir = str(os.path.expanduser("~")+"/")
        self.record_file_path = record_file_path = "/Documents/UBA/proyectoSDR/flowgraphs/recordings/"
        self.centerFreq = centerFreq = 1090e3+offset
        self.timestamp = timestamp = datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S')
        self.taps_sca = taps_sca = firdes.low_pass(2, samp_rate, 6e3,2e3, window.WIN_KAISER, 6.76)
        self.rec_button = rec_button = 0
        self.filename = filename = rootdir+record_file_path+"_"+"Station1:"+str(int(centerFreq+station1-125e6))+"Hz_""Station2:"+str(int(centerFreq+station2-125e6))+"Hz_"+str(int(samp_rate))+"sps_"
        self.center_freq = center_freq = 1e6

        ##################################################
        # Blocks
        ##################################################

        # Create the options list
        self._station2_options = [580000.0, 610000.0, 650000.0, 690000.0, 730000.0, 770000.0, 810000.0, 850000.0, 890000.0, 930000.0, 970000.0, 1010000.0, 1050000.0, 1090000.0, 1130000.0, 1170000.0, 1250000.0, 1290000.0, 1330000.0, 1410000.0, 1450000.0]
        # Create the labels list
        self._station2_labels = ['Clarin 580', 'Rural 610', 'Clasica 650', 'Sarandi 690', 'Continente 730', 'Oriental 770', 'Espectador 810', 'Carve 850', 'Sport 890', 'Monte Carlo 930', 'Universal 970', 'Deportiva 1010', 'Uruguay 1050', 'Maria 1090', 'Nacional 1130', 'Radiomundo 1170', 'Centenario 1250', 'Cultura 1290', 'Fenix 1330', 'La R 1410', 'America 1450']
        # Create the combo box
        self._station2_tool_bar = Qt.QToolBar(self)
        self._station2_tool_bar.addWidget(Qt.QLabel("'station2'" + ": "))
        self._station2_combo_box = Qt.QComboBox()
        self._station2_tool_bar.addWidget(self._station2_combo_box)
        for _label in self._station2_labels: self._station2_combo_box.addItem(_label)
        self._station2_callback = lambda i: Qt.QMetaObject.invokeMethod(self._station2_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._station2_options.index(i)))
        self._station2_callback(self.station2)
        self._station2_combo_box.currentIndexChanged.connect(
            lambda i: self.set_station2(self._station2_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._station2_tool_bar)
        # Create the options list
        self._station1_options = [580000.0, 610000.0, 650000.0, 690000.0, 730000.0, 770000.0, 810000.0, 850000.0, 890000.0, 930000.0, 970000.0, 1010000.0, 1050000.0, 1090000.0, 1130000.0, 1170000.0, 1250000.0, 1290000.0, 1330000.0, 1410000.0, 1450000.0]
        # Create the labels list
        self._station1_labels = ['Clarin 580', 'Rural 610', 'Clasica 650', 'Sarandi 690', 'Continente 730', 'Oriental 770', 'Espectador 810', 'Carve 850', 'Sport 890', 'Monte Carlo 930', 'Universal 970', 'Deportiva 1010', 'Uruguay 1050', 'Maria 1090', 'Nacional 1130', 'Radiomundo 1170', 'Centenario 1250', 'Cultura 1290', 'Fenix 1330', 'La R 1410', 'America 1450']
        # Create the combo box
        self._station1_tool_bar = Qt.QToolBar(self)
        self._station1_tool_bar.addWidget(Qt.QLabel("'station1'" + ": "))
        self._station1_combo_box = Qt.QComboBox()
        self._station1_tool_bar.addWidget(self._station1_combo_box)
        for _label in self._station1_labels: self._station1_combo_box.addItem(_label)
        self._station1_callback = lambda i: Qt.QMetaObject.invokeMethod(self._station1_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._station1_options.index(i)))
        self._station1_callback(self.station1)
        self._station1_combo_box.currentIndexChanged.connect(
            lambda i: self.set_station1(self._station1_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._station1_tool_bar)
        self._rec_button_choices = {'Pressed': 1, 'Released': 0}

        _rec_button_toggle_button = qtgui.ToggleButton(self.set_rec_button, 'RECORD', self._rec_button_choices, False, 'value')
        _rec_button_toggle_button.setColors("green", "default", "red", "default")
        self.rec_button = _rec_button_toggle_button

        self.top_grid_layout.addWidget(_rec_button_toggle_button, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq((center_freq+offset), 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=3,
                decimation=8,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=3,
                decimation=8,
                taps=[],
                fractional_bw=0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.network_tcp_sink_0_0 = network.tcp_sink(gr.sizeof_float, 1, '127.0.0.1', 1235,2)
        self.network_tcp_sink_0 = network.tcp_sink(gr.sizeof_float, 1, '127.0.0.1', 1234,2)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(4, taps_sca, (station2-center_freq), samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(4, taps_sca, (station1-center_freq), samp_rate)
        self._centerFreq_range = qtgui.Range(570e3+offset, 1450e3+offset, 40e3, 1090e3+offset, 200)
        self._centerFreq_win = qtgui.RangeWidget(self._centerFreq_range, self.set_centerFreq, "'centerFreq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._centerFreq_win)
        self.blocks_wavfile_sink_0_0 = blocks.wavfile_sink(
            filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+".wav" if rec_button == 1 else "/dev/null",
            2,
            48000,
            blocks.FORMAT_WAV,
            blocks.FORMAT_PCM_16,
            False
            )
        self.analog_am_demod_cf_0_0 = analog.am_demod_cf(
        	channel_rate=240000,
        	audio_decim=5,
        	audio_pass=2e3,
        	audio_stop=5e3,
        )
        self.analog_am_demod_cf_0 = analog.am_demod_cf(
        	channel_rate=240000,
        	audio_decim=5,
        	audio_pass=2e3,
        	audio_stop=5e3,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_am_demod_cf_0, 0), (self.blocks_wavfile_sink_0_0, 0))
        self.connect((self.analog_am_demod_cf_0, 0), (self.network_tcp_sink_0, 0))
        self.connect((self.analog_am_demod_cf_0_0, 0), (self.blocks_wavfile_sink_0_0, 1))
        self.connect((self.analog_am_demod_cf_0_0, 0), (self.network_tcp_sink_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_am_demod_cf_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_am_demod_cf_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "radioAppAM")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.set_centerFreq(1090e3+self.offset)
        self.rtlsdr_source_0.set_center_freq((self.center_freq+self.offset), 0)

    def get_station2(self):
        return self.station2

    def set_station2(self, station2):
        self.station2 = station2
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1-125e6))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2-125e6))+"Hz_"+str(int(self.samp_rate))+"sps_")
        self._station2_callback(self.station2)
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq((self.station2-self.center_freq))

    def get_station1(self):
        return self.station1

    def set_station1(self, station1):
        self.station1 = station1
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1-125e6))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2-125e6))+"Hz_"+str(int(self.samp_rate))+"sps_")
        self._station1_callback(self.station1)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((self.station1-self.center_freq))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1-125e6))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2-125e6))+"Hz_"+str(int(self.samp_rate))+"sps_")
        self.set_taps_sca(firdes.low_pass(2, self.samp_rate, 6e3, 2e3, window.WIN_KAISER, 6.76))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_rootdir(self):
        return self.rootdir

    def set_rootdir(self, rootdir):
        self.rootdir = rootdir
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1-125e6))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2-125e6))+"Hz_"+str(int(self.samp_rate))+"sps_")

    def get_record_file_path(self):
        return self.record_file_path

    def set_record_file_path(self, record_file_path):
        self.record_file_path = record_file_path
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1-125e6))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2-125e6))+"Hz_"+str(int(self.samp_rate))+"sps_")

    def get_centerFreq(self):
        return self.centerFreq

    def set_centerFreq(self, centerFreq):
        self.centerFreq = centerFreq
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1-125e6))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2-125e6))+"Hz_"+str(int(self.samp_rate))+"sps_")

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_taps_sca(self):
        return self.taps_sca

    def set_taps_sca(self, taps_sca):
        self.taps_sca = taps_sca
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.taps_sca)
        self.freq_xlating_fir_filter_xxx_0_0.set_taps(self.taps_sca)

    def get_rec_button(self):
        return self.rec_button

    def set_rec_button(self, rec_button):
        self.rec_button = rec_button
        self.blocks_wavfile_sink_0_0.open(self.filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+".wav" if self.rec_button == 1 else "/dev/null")

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename
        self.blocks_wavfile_sink_0_0.open(self.filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+".wav" if self.rec_button == 1 else "/dev/null")

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((self.station1-self.center_freq))
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq((self.station2-self.center_freq))
        self.rtlsdr_source_0.set_center_freq((self.center_freq+self.offset), 0)




def main(top_block_cls=radioAppAM, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
