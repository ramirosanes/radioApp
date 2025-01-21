#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: radioApp
# Author: pi
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
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



class radioApp(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "radioApp", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("radioApp")
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

        self.settings = Qt.QSettings("GNU Radio", "radioApp")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.double_station = double_station = False
        self.station2 = station2 = -400000 if double_station == 1 else 0
        self.station1 = station1 = 400000 if double_station == 1 else 0
        self.samp_rate = samp_rate = 2560000
        self.rootdir = rootdir = str(os.path.expanduser("~")+"/")
        self.rfGain = rfGain = 25
        self.record_file_path = record_file_path = "/Documents/UBA/proyectoSDR/flowgraphs/recordings/"
        self.centerFreq = centerFreq = 94300000
        self.timestamp = timestamp = datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S')
        self.taps = taps = firdes.low_pass(1.0, samp_rate, 100000,10000, window.WIN_HAMMING, 6.76)
        self.rec_button = rec_button = 0
        self.filename = filename = rootdir+record_file_path+"_"+"Station1:"+str(int(centerFreq+station1))+"Hz_""Station2:"+str(int(centerFreq+station2))+"Hz_"+str(int(samp_rate))+"sps_"+str(rfGain)+"dB_"

        ##################################################
        # Blocks
        ##################################################

        self._double_station_choices = {'Pressed': 1, 'Released': 0}

        _double_station_toggle_button = qtgui.ToggleButton(self.set_double_station, 'double_station', self._double_station_choices, False, 'value')
        _double_station_toggle_button.setColors("green", "default", "red", "default")
        self.double_station = _double_station_toggle_button

        self.top_grid_layout.addWidget(_double_station_toggle_button, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._station2_range = qtgui.Range(-1200000, 1200000, 200000, -400000 if double_station == 1 else 0, 200)
        self._station2_win = qtgui.RangeWidget(self._station2_range, self.set_station2, "'station2'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._station2_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._station1_range = qtgui.Range(-1200000, 1200000, 200000, 400000 if double_station == 1 else 0, 200)
        self._station1_win = qtgui.RangeWidget(self._station1_range, self.set_station1, "'station1'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._station1_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rfGain_range = qtgui.Range(0, 30, 0.1, 25, 200)
        self._rfGain_win = qtgui.RangeWidget(self._rfGain_range, self.set_rfGain, "RF Gain (dB)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rfGain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._rec_button_choices = {'Pressed': 1, 'Released': 0}

        _rec_button_toggle_button = qtgui.ToggleButton(self.set_rec_button, 'RECORD', self._rec_button_choices, False, 'value')
        _rec_button_toggle_button.setColors("green", "default", "red", "default")
        self.rec_button = _rec_button_toggle_button

        self.top_grid_layout.addWidget(_rec_button_toggle_button, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._centerFreq_range = qtgui.Range(88300000, 108900000, 200000, 94300000, 200)
        self._centerFreq_win = qtgui.RangeWidget(self._centerFreq_range, self.set_centerFreq, "'centerFreq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._centerFreq_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(centerFreq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(rfGain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
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
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
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

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 6, 0, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.network_tcp_sink_0_0 = network.tcp_sink(gr.sizeof_float, 1, '127.0.0.1', 1235,2)
        self.network_tcp_sink_0 = network.tcp_sink(gr.sizeof_float, 1, '127.0.0.1', 1234,2)
        self.freq_xlating_fft_filter_ccc_0_0 = filter.freq_xlating_fft_filter_ccc(10, taps, station1, samp_rate)
        self.freq_xlating_fft_filter_ccc_0_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0_0.declare_sample_delay(0)
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(10, taps, station2, samp_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self.blocks_wavfile_sink_0_0 = blocks.wavfile_sink(
            filename+str(datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S'))+".wav" if rec_button == 1 else "/dev/null",
            2,
            48000,
            blocks.FORMAT_WAV,
            blocks.FORMAT_PCM_16,
            False
            )
        self.analog_wfm_rcv_0_0 = analog.wfm_rcv(
        	quad_rate=256000,
        	audio_decimation=5,
        )
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=256000,
        	audio_decimation=5,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_wavfile_sink_0_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.network_tcp_sink_0, 0))
        self.connect((self.analog_wfm_rcv_0_0, 0), (self.blocks_wavfile_sink_0_0, 1))
        self.connect((self.analog_wfm_rcv_0_0, 0), (self.network_tcp_sink_0_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.analog_wfm_rcv_0_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fft_filter_ccc_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "radioApp")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_double_station(self):
        return self.double_station

    def set_double_station(self, double_station):
        self.double_station = double_station
        self.set_station1(400000 if self.double_station == 1 else 0)
        self.set_station2(-400000 if self.double_station == 1 else 0)

    def get_station2(self):
        return self.station2

    def set_station2(self, station2):
        self.station2 = station2
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.rfGain)+"dB_")
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.station2)

    def get_station1(self):
        return self.station1

    def set_station1(self, station1):
        self.station1 = station1
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.rfGain)+"dB_")
        self.freq_xlating_fft_filter_ccc_0_0.set_center_freq(self.station1)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.rfGain)+"dB_")
        self.set_taps(firdes.low_pass(1.0, self.samp_rate, 100000, 10000, window.WIN_HAMMING, 6.76))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_rootdir(self):
        return self.rootdir

    def set_rootdir(self, rootdir):
        self.rootdir = rootdir
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.rfGain)+"dB_")

    def get_rfGain(self):
        return self.rfGain

    def set_rfGain(self, rfGain):
        self.rfGain = rfGain
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.rfGain)+"dB_")
        self.rtlsdr_source_0.set_gain(self.rfGain, 0)

    def get_record_file_path(self):
        return self.record_file_path

    def set_record_file_path(self, record_file_path):
        self.record_file_path = record_file_path
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.rfGain)+"dB_")

    def get_centerFreq(self):
        return self.centerFreq

    def set_centerFreq(self, centerFreq):
        self.centerFreq = centerFreq
        self.set_filename(self.rootdir+self.record_file_path+"_"+"Station1:"+str(int(self.centerFreq+self.station1))+"Hz_""Station2:"+str(int(self.centerFreq+self.station2))+"Hz_"+str(int(self.samp_rate))+"sps_"+str(self.rfGain)+"dB_")
        self.rtlsdr_source_0.set_center_freq(self.centerFreq, 0)

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.freq_xlating_fft_filter_ccc_0.set_taps(self.taps)
        self.freq_xlating_fft_filter_ccc_0_0.set_taps(self.taps)

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




def main(top_block_cls=radioApp, options=None):

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
