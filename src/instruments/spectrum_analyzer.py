from src.core import Instrument, Parameter
import visa
import numpy as np
import time


class SpectrumAnalyzer(Instrument):
    """
    This class provides a python implementation of the Keysight N9320B 9kHz-3.0GHz spectrum analyzer
    with trigger generator.
    """

    _INSTRUMENT_IDENTIFIER = u'Keysight Technologies,N9320B,CN0323B356,0B.03.58'
    # String returned by spectrum analyzer upon querying it with '*IDN?'

    _DEFAULT_SETTINGS = Parameter([
            Parameter('visa_resource', 'USB0::0x0957::0xFFEF::CN0323B356::INSTR', (str),
                      'pyVisa instrument identifier, to make a connection using the pyVisa package.'),
            Parameter('start_frequency', 0.0, float, 'start frequency of spectrum analyzer frequency range'),
            Parameter('mode', 'SpectrumAnalyzer', ['SpectrumAnalyzer', 'TrackingGenerator'],
                      'switches between normal spectrum analyzer mode or spectrum analyzer PLUS output, '
                      'i.e., tracking generator'),
            Parameter('stop_frequency', 3e9, float, 'stop frequency of spectrum analyzer frequency range'),
            Parameter('output_on', True, bool, 'toggles the tracking generator'),
            Parameter('connection_timeout', 1000, int, 'the time to wait for a response '
                                                       'from the spectrum analyzer with each query'),
            Parameter('output_power', 10.0, float, 'the output power (in dBm) of the tracking generator')
        ])

    def __init__(self, name='SpectrumAnalyzer', settings={}):
        """

        Args:
            name (str): optional name of instance of class
            settings (list): list of other values to initialize class with

        """
        super(SpectrumAnalyzer, self).__init__(name, settings)

        rm = visa.ResourceManager()
        self.spec_anal = rm.open_resource(self.settings['visa_resource'])
        self.spec_anal.read_termination = '\n'
        self.spec_anal.timeout = self.settings['connection_timeout']
        self.spec_anal.write('*RST;*OPC?;*CLS')
        time.sleep(5)
        self._set_mode('SpectrumAnalyzer')
        time.sleep(5)
        print 'hi'

    def update(self, settings):
        super(SpectrumAnalyzer, self).update(settings)

        for key, value in settings.iteritems():
            if key == 'start_frequency':
                self._set_start_frequency(value)
            elif key == 'stop_frequency':
                self._set_stop_frequency(value)
            elif key == 'output_on':
                self._toggle_output(value)
            elif key == 'output_power':
                self._set_output_power(value)
            elif key == 'mode':
                self._set_mode(value)
            else:
                message = '{0} is not a parameter of {1}'.format(key, self.name)

    @property
    def _probes(self):
        probes = {'start_frequency': 'the lower bound of the frequency sweep',
                  'stop_frequency': 'the upper bound of the frequency sweep',
                  'trace': 'the frequency sweep of the inputted signal',
                  'tracking_generator': 'checks if the tracking generator is on',
                  'bandwidth': 'the curent bandwidth of the spectrum analyzer',
                  'output_power': 'the power of the tracking generator',
                  'mode': 'Spectrum Analyzer Mode or Tracking Generator Mode'}

    def read_probes(self, probe_name):
        if probe_name == 'start_frequency':
            return self._get_start_frequency()
        elif probe_name == 'stop_frequency':
            return self._get_stop_frequency()
        elif probe_name == 'trace':
            return self._get_trace()
        elif probe_name == 'output_on':
            return self._is_output_on()
        elif probe_name == 'bandwidth':
            return self._get_bandwidth()
        elif probe_name == 'output_power':
            return self._get_output_power()
        elif probe_name == 'mode':
            return self._get_mode()
        else:
            message = 'no probe with that name exists!'
            raise AttributeError(message)

    def is_connected(self):
        """
        Checks if the instrument is connected.
        Returns: True if connected, False otherwise.

        """
        identification = self.spec_anal.query('*IDN?\n'+ ';*OPC?')
        print identification
        return identification == self._INSTRUMENT_IDENTIFIER

    def _set_start_frequency(self, start_freq):
        self.spec_anal.write('SENS:FREQ:START ' + str(start_freq) + ';*OPC?')

    def _get_start_frequency(self):
        return float(self.spec_anal.query('SENS:FREQ:START?\n' + ';*OPC?'))

    def _set_stop_frequency(self, stop_freq):
        self.spec_anal.write('SENS:FREQ:STOP ' + str(stop_freq)+ ';*OPC?')

    def _get_stop_frequency(self):
        return float(self.spec_anal.query('SENS:FREQ:STOP?\n' + ';*OPC?'))

    def _toggle_output(self, state):
        if state:
            self.spec_anal.write('OUTPUT 1' + ';*OPC?')
        elif not state:
            self.spec_anal.write('OUTPUT 0' + ';*OPC?')

    def _is_output_on(self):
        if self.mode == 'SpectrumAnalyzer':
            return False
        elif self.mode == 'TrackingGenerator':
            return bool(int(self.spec_anal.query('OUTPUT:STATE?' + ';*OPC?')))

    def _get_mode(self):
        mode_response = str(self.spec_anal.query('CONFIGURE?' + ';*OPC?')).strip()
        if mode_response == 'SAN':
            return 'SpectrumAnalyzer'
        elif mode_response == 'TGEN':
            return 'TrackingGenerator'

    def _set_mode(self, mode):
        if mode == 'TrackingGenerator':
            self.spec_anal.write('CONFIGURE:TGENERATOR' + ';*OPC?')
        elif mode == 'SpectrumAnalyzer':
            self.spec_anal.write('CONFIGURE:SANALYZER' + ';*OPC?')

    def _get_trace(self):
        amplitudes = [float(i) for i in str(self.spec_anal.query('TRACE:DATA? TRACE1'+ ';*OPC?')).split(',')]
        num_points = len(amplitudes)
        frequencies = np.linspace(start=self.start_frequency, stop=self.stop_frequency,
                                  num=num_points)
        return np.array([(frequencies[i], amplitudes[i])for i in range(num_points)])

    def _get_bandwidth(self):
        return float(self.spec_anal.query('BANDWIDTH?' + ';*OPC?'))

    def _get_output_power(self):
        return self.spec_anal.query('SOURCE:POWER?' + ';*OPC?')

    def set_output_power(self, power):
        return self.spec_anal.write('SOURCE:POWER ' + str(power) + ';*OPC?')

    def __del__(self):
        self._set_mode('SpectrumAnalyzer' + ';*OPC?')
        self.spec_anal.close()

if __name__ == '__main__':

        spec_anal = SpectrumAnalyzer()
        print spec_anal.is_connected()
        spec_anal.mode = 'TrackingGenerator'
        print spec_anal.output_on
        spec_anal.output_on = True
        print spec_anal.output_on

