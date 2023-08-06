#! /usr/bin/python3
# -*- coding: utf-8 -*-


"""
    *************************
    Observation configuration
    *************************

    Backend setup
    -------------
    
    Manual setting
    ^^^^^^^^^^^^^^

    Setting from Parset file
    ^^^^^^^^^^^^^^^^^^^^^^^^

    Observation setup
    -----------------

    Single observation
    ^^^^^^^^^^^^^^^^^^

    List of observations
    ^^^^^^^^^^^^^^^^^^^^

    Classes summary
    ---------------

    .. autosummary::
        :nosignatures:

        ~nenupy.observation.obs_config.ObsConfig
        ~nenupy.observation.obs_config.BSTConfig
        ~nenupy.observation.obs_config.NICKELConfig
        ~nenupy.observation.obs_config.TFConfig
        ~nenupy.observation.obs_config.PulsarFoldConfig

"""


__author__ = 'Alan Loh, Baptiste Cecconi'
__copyright__ = 'Copyright 2020, nenupy'
__credits__ = ['Alan Loh']
__maintainer__ = 'Alan'
__email__ = 'alan.loh@obspm.fr'
__status__ = 'Production'
__all__ = [
    'BSTConfig',
    'NICKELConfig',
    'TFConfig',
    'PulsarFoldConfig',
    'ObsConfig'
]


import astropy.units as u
from astropy.time import TimeDelta
import numpy as np

from nenupy.observation import Parset
from nenupy.miscellaneous import accepts

import logging
log = logging.getLogger(__name__)


backendProperties = {
    'nickel': {
        'nSubBands': {
            'min': 1,
            'max': 384,
            'default': 384,
            'type': '`int`',
            'desc': 'Number of sub-bands'
        },
        'nChannels': {
            'min': 1,
            'max': 64,
            'default': 64,
            'type': '`int`',
            'desc': 'Number of channels'
        },
        'nPolars': {
            'min': 1,
            'max': 4,
            'default': 4,
            'type': '`int`',
            'desc': 'Number of polarizations'
        },
        'nMAs': {
            'min': 2,
            'max': 96 + 6,
            'default': 96,
            'type': '`int`',
            'desc': 'Number of Mini-Arrays'
        },
        'timeRes': {
            'min': 0.,
            'max': 10.,
            'default': 1.,
            'type': '`float` or :class:`~astropy.time.TimeDelta`',
            'desc': 'Time resolution in seconds'
        }
    },
    #'raw': {},
    'tf': {
        'nPolars': {
            'min': 1,
            'max': 4,
            'default': 4,
            'type': '`int`',
            'desc': 'Number of polarizations'
        },
        'timeRes': {
            'min': (0.30*u.ms).to(u.s).value,
            'max': (84.00*u.ms).to(u.s).value,
            'default': (5.00*u.ms).to(u.s).value,
            'type': '`float` or :class:`~astropy.time.TimeDelta`',
            'desc': 'Time resolution in seconds'
        },
        'freqRes': {
            'min': (0.10*u.kHz).to(u.Hz).value,
            'max': (12.20*u.kHz).to(u.Hz).value,
            'default': (6.10*u.kHz).to(u.Hz).value,
            'type': '`float` or :class:`~astropy.units.Quantity`',
            'desc': 'Frequency resolution in Hz'
        },
        'nSubBands': {
            'min': 1,
            'max': 768,
            'default': 768,
            'type': '`int`',
            'desc': 'Number of sub-bands'
        },
    },
    'bst': {
        'nSubBands': {
            'min': 1,
            'max': 768,
            'default': 768,
            'type': '`int`',
            'desc': 'Number of sub-bands'
        },
        'nPolars': {
            'min': 1,
            'max': 2,
            'default': 2,
            'type': '`int`',
            'desc': 'Number of polarizations'
        }
    },
    # 'sst': {},
    'pulsar_fold': {
        'nChannels': {
            'min': 1,
            'max': 192,
            'default': 192,
            'type': '`int`',
            'desc': 'Number of channels'
        },
        'nPolars': {
            'min': 1,
            'max': 4,
            'default': 4,
            'type': '`int`',
            'desc': 'Number of polarizations'
        },
        'tFold': {
            'min': 5.36870912,
            'max': 21.47483648,
            'default': 10.73741824,
            'type': '`float` or :class:`~astropy.time.TimeDelta`',
            'desc': 'Pulsar time fold in seconds'
        },
        'nBins': {
            'min': 16,
            'max': 8096,
            'default': 2048,
            'type': '`int`',
            'desc': 'Number of bins'
        }
    },
    # 'pulsar_waveolaf': {},
    # 'pulsar_single': {
    #     'nChannels': {
    #         'min': 1,
    #         'max': 192,
    #         'default': 192
    #     },
    #     'nPolars': {
    #         'min': 1,
    #         'max': 4,
    #         'default': 4
    #     },
    #     'nBits': {
    #         'min': ,
    #         'max': ,
    #         'default': 
    #     },
    #     'dsTime': {
    #         'min': 1,
    #         'max': 128,
    #         'default': 128
    #     }, # dstime corespond au downsampling il peut prendre les valeurs (1, 2, 4, 8, 16, 32, 64, 128)
    # }
}


complex64 = np.complex64().itemsize * u.byte
float32 = np.float32().itemsize * u.byte


def doc(docstring, backend):
    prop = backendProperties[backend]
    paramDoc = ''
    for key in prop.keys():
        param = prop[key]
        paramDoc += f"""
            :param {key}:
                {param['desc']} (min: ``{param['min']}``,
                max: ``{param['max']}``, default: ``{param['default']}``).
            :type {key}: {param['type']}
        """
    paramDoc += """
            :param durationSec:
                Observation duration in seconds (default: ``0``).
            :type durationSec: `int` or :class:`~astropy.time.TimeDelta`
    """
    def document(func):
        func.__doc__ = docstring + '\n' + paramDoc
        return func
    return document


# ============================================================= #
# ---------------------- _BackendConfig ----------------------- #
# ============================================================= #
class _BackendConfig(object):
    """
    """

    def __init__(self, backend, **kwargs):
        self.durationSec = kwargs.get(
            'durationSec',
            0
        )
        self._backend = backend

        # Catch the irrelevant kwargs
        for attr in kwargs.keys():
            if attr.startswith('_'):
                raise AttributeError(
                    "Attribute '{}' starting with '_' cannot be set.".format(
                        attr
                    )
                )
            if attr not in dir(self):
                raise AttributeError(
                    "'{}' object has no attribute '{}'".format(
                        self.__class__.__name__,
                        attr
                    )
                )

        # Fill the relevant kwargs
        for attr in backendProperties[self._backend].keys():
            setattr(
                self,
                attr,
                kwargs.get(
                    attr,
                    backendProperties[self._backend][attr]['default']
                )
            )


    def __str__(self):
        className = self.__class__.__name__
        title = "Backend configuration of type '{}'\n".format(className)
        attributes = [att for att in dir(self) if not att.startswith('_')]
        properties = 'Properties: '
        for att in attributes:
            properties += "'{}={}', ".format(att, getattr(self, att))
        properties = properties[:-2] # remove the last coma
        properties += '\n'
        return title + properties


    # --------------------------------------------------------- #
    # --------------------- Getter/Setter --------------------- #
    @property
    def nSubBands(self):
        """
        """
        return self._nSubBands
    @nSubBands.setter
    @accepts(object, int)
    def nSubBands(self, nsb):
        self._nSubBands = self._checkAttr(
            key='nSubBands',
            value=nsb,
            name='sub-bands'
        )


    @property
    def nChannels(self):
        """
        """
        return self._nChannels
    @nChannels.setter
    @accepts(object, int)
    def nChannels(self, chan):
        self._nChannels = self._checkAttr(
            key='nChannels',
            value=chan,
            name='channels'
        )


    @property
    def nPolars(self):
        """
        """
        return self._nPolars
    @nPolars.setter
    @accepts(object, int)
    def nPolars(self, np):
        self._nPolars = self._checkAttr(
            key='nPolars',
            value=np,
            name='polarizations'
        )


    @property
    def timeRes(self):
        """
        """
        return self._timeRes
    @timeRes.setter
    @accepts(object, (float, int, TimeDelta))
    def timeRes(self, dt):
        if isinstance(dt, TimeDelta):
            dt = dt.sec
        self._timeRes = self._checkAttr(
            key='timeRes',
            value=dt,
            name='time resolution'
        )


    @property
    def freqRes(self):
        """
        """
        return self._freqRes
    @freqRes.setter
    @accepts(object, (float, int, u.Quantity))
    def freqRes(self, df):
        if isinstance(df, u.Quantity):
            df = df.to(u.Hz).value
        self._freqRes = self._checkAttr(
            key='freqRes',
            value=df,
            name='frequency resolution'
        )


    @property
    def nMAs(self):
        """
        """
        return self._nMAs
    @nMAs.setter
    @accepts(object, int)
    def nMAs(self, ma):
        self._nMAs = self._checkAttr(
            key='nMAs',
            value=ma,
            name='Mini-Arrays'
        )


    @property
    def durationSec(self):
        """
        """
        return self._durationSec
    @durationSec.setter
    @accepts(object, (float, int, TimeDelta), strict=False)
    def durationSec(self, s):
        if isinstance(s, TimeDelta):
            s = s.sec
        self._durationSec = s


    # --------------------------------------------------------- #
    # ------------------------ Methods ------------------------ #


    # --------------------------------------------------------- #
    # ----------------------- Internal ------------------------ #
    def _checkAttr(self, key, value, name):
        attrProp = backendProperties[self._backend][key]
        minVal = attrProp['min']
        maxVal = attrProp['max']
        defaultVal = attrProp['default']
        if value > maxVal:
            log.warning(
                "Maximal value of {0} is {1}. Setting to default '{2}={3}'.".format(
                    name,
                    maxVal,
                    key,
                    defaultVal
                )
            )
            value = defaultVal
        elif value < minVal:
            log.warning(
                "Minimal value for {0} is {1}. Setting to default '{2}={3}'.".format(
                    name,
                    minVal,
                    key,
                    defaultVal
                )
            )
            value = defaultVal
        return value
# ============================================================= #
# ============================================================= #


# ============================================================= #
# ------------------------- BSTConfig ------------------------- #
# ============================================================= #
@doc('Beamlet Statistics observation configuration.', 'bst')
class BSTConfig(_BackendConfig):
    
    def __init__(self, **kwargs):
        super().__init__(backend='bst', **kwargs)


    # --------------------------------------------------------- #
    # --------------------- Getter/Setter --------------------- #
    @property
    def volume(self):
        """
        """
        nElements = self.nPolars * self.durationSec * self.nSubBands
        return (nElements * float32).to(u.Mibyte)


    # --------------------------------------------------------- #
    # ------------------------ Methods ------------------------ #
    @classmethod
    @accepts(type, (Parset, str))
    def fromParset(cls, parset):
        """ 

            :param parset:
                Observation parset file.
            :type parset: `str` or :class:`~nenupy.observation.parset.Parset`

            :returns:
                Backend configuration as defined by the ``parset`` file.
            :rtype: :class:`~nenupy.observation.obs_config.BSTConfig`

        """
        if isinstance(parset, str):
            parset = Parset(parset)

        dbeams = parset.digibeams
        
        # Find out the total duration of observation
        # Loop over the digibeams, as they can be simultaneous
        totalTimes = np.array([])
        for db in dbeams.keys():
            dts = TimeDelta(
                np.arange(dbeams[db]['duration']),
                format='sec'
            )
            dbTimes = dbeams[db]['startTime'] + dts
            totalTimes = np.union1d(totalTimes, dbTimes.jd)
        
        return BSTConfig(
            durationSec=totalTimes.size
        )
# ============================================================= #
# ============================================================= #


# ============================================================= #
# ----------------------- NICKELConfig ------------------------ #
# ============================================================= #
@doc('NICKEL correlator observation configuration.', 'nickel')
class NICKELConfig(_BackendConfig):
    """
    """

    def __init__(self, **kwargs):
        super().__init__(backend='nickel', **kwargs)


    # --------------------------------------------------------- #
    # --------------------- Getter/Setter --------------------- #
    @property
    def volume(self):
        """
        """
        nBaselines = self.nMAs * (self.nMAs - 1)/2 + self.nMAs
        visVolume = self.nPolars * nBaselines * complex64
        ratePerSB = visVolume * self.nChannels / self.timeRes
        ratePerObs = ratePerSB * self.nSubBands
        return (ratePerObs * self.durationSec).to(u.Gibyte)


    # --------------------------------------------------------- #
    # ------------------------ Methods ------------------------ #
    @classmethod
    @accepts(type, (Parset, str))
    def fromParset(cls, parset):
        """
        """
        if isinstance(parset, str):
            parset = Parset(parset)

        out = parset.output
        anabeams = parset.anabeams

        if 'nri_receivers' not in out.keys():
            # Nickel receiver has not been used
            return NICKELConfig()
        elif 'nickel' not in out['nri_receivers']:
            # Nickel receiver has not been used
            return NICKELConfig()

        # Hypothesis that only one analog beam is used!
        return NICKELConfig(
            durationSec=anabeams[0]['duration'],
            timeRes=out['nri_dumpTime'],
            nSubBands=len(out['nri_subbandList']),
            nChannels=out['nri_channelization'],
            nMAs=len(anabeams[0]['maList']),
        )
        #767G   20201208_061100_20201208_081400_VIR_A_TRACKING/
        #24G    SB150.MS/
# ============================================================= #
# ============================================================= #


# ============================================================= #
# --------------------- _UnDySPuTeDConfig --------------------- #
# ============================================================= #
class _UnDySPuTeDConfig(_BackendConfig):
    """
    """

    def __init__(self, backend, **kwargs):
        super().__init__(backend=backend, **kwargs)


    # --------------------------------------------------------- #
    # ----------------------- Internal ------------------------ #
    def _parseParameters(self, parameters):
        """ Parse values from the digital beam 'parameters'
            entry.
            E.g. 'TF: DF=3.05 DT=10.0 HAMM'
        """
        parameters = parameters.lower()
        mode = parameters.split(':')[0]
        configs = {
            param.split('=')[0]: param.split('=')[1]\
            for param in parameters.split()\
            if '=' in param
        }
        return mode, configs


    # --------------------------------------------------------- #
    # ----------------------- Internal ------------------------ #
    @staticmethod
    @accepts((float, int, u.Quantity), (float, int, u.Quantity))
    def _checkDFvsDT(dt, df):
        """ Short time resolutions are impossible for narrow
            frequency resolutions. Some df/dt combinations are
            therefore not allowed.
        """
        if isinstance(dt, u.Quantity):
            dt = dt.to(u.s).value
        if isinstance(df, u.Quantity):
            df = df.to(u.Hz).value

        allowedFftlen = 2**( np.arange(8) + 4 )
        allowedNfft2int = 2**(np.arange(9) + 2)
        
        # Find the closest fftlen to the desired df value
        fftlen = allowedFftlen[
            np.argmin(
                np.abs(allowedFftlen - 1.0 / 5.12e-6 / df) # 1/(5.12e-6 s) = 195312.5 Hz
            )
        ]

        # Find the closest nfft2int to the desired df value
        nfft2int = allowedNfft2int[
            np.argmin(
                np.abs(allowedNfft2int - dt / (5.12e-6 * fftlen))
            )
        ]

        dtEff = 5.12e-6 * fftlen * nfft2int
        dfEff = 1.0 / 5.12e-6 / fftlen

        log.info(
            "'freqRes={0:.2f}', 'timeRes={1:.2f}' <--> 'df={2:.2f}', 'dt={3:.2f}' ('fftlen={4}', 'nfft2int={5}')".format(
                (df*u.Hz).to(u.kHz),
                (dt*u.s).to(u.ms),
                (dfEff*u.Hz).to(u.kHz),
                (dtEff*u.s).to(u.ms),
                fftlen,
                nfft2int
            )
        )

        return dtEff, dfEff
# ============================================================= #
# ============================================================= #


# ============================================================= #
# ------------------------ _BeamConfig ------------------------ #
# ============================================================= #
class _TFBeamConfig(_BackendConfig):
    """
    """

    def __init__(self, **kwargs):
        super().__init__(backend='tf', **kwargs)


    # --------------------------------------------------------- #
    # --------------------- Getter/Setter --------------------- #
    @property
    def volume(self):
        """
        """
        ratePerSB = self.nPolars * float32 * (200.e6/1024./self.freqRes) / self.timeRes
        rateObs = ratePerSB * self.nSubBands
        return (rateObs * self.durationSec).to(u.Gibyte)
# ============================================================= #
# ============================================================= #


# ============================================================= #
# ------------------------- TFConfig -------------------------- #
# ============================================================= #
@doc('UnDySPuTeD Time-Frequency mode observation configuration.', 'tf')
class TFConfig(_UnDySPuTeDConfig):
    """
    """

    def __init__(self, _setFromParset=False, **kwargs):
        if not _setFromParset:
            super().__init__(backend='tf', **kwargs)
            self.timeRes, self.freqRes = self._checkDFvsDT(
                dt=self.timeRes,
                df=self.freqRes
            )
            kwargs['timeRes'] = self.timeRes
            kwargs['freqRes'] = self.freqRes
            self._beamConfigs = [
                _TFBeamConfig(**kwargs)
            ]
        else:
            self._beamConfigs = []


    # --------------------------------------------------------- #
    # --------------------- Getter/Setter --------------------- #
    @property
    def volume(self):
        """
        """
        vol = 0 * u.Gibyte
        for bc in self._beamConfigs:
            vol += bc.volume
        return vol


    # --------------------------------------------------------- #
    # ------------------------ Methods ------------------------ #
    @classmethod
    @accepts(type, (str, Parset))
    def fromParset(cls, parset):
        """
        """
        if isinstance(parset, str):
            parset = Parset(parset)

        out = parset.output
        digibeams = parset.digibeams

        tf = TFConfig(_setFromParset=True)
        beamConfigs = []
        
        if 'undysputed' not in out['hd_receivers']:
            # UnDySPuTeD receiver has not been used
            beamConfigs.append(
                _TFBeamConfig()
            )
        else:
            for db in digibeams.keys():
                if digibeams[db]['toDo'].lower() != 'dynamicspectrum':
                    continue
                mode, parameters = tf._parseParameters(digibeams[db]['parameters'])
                if mode != 'tf':
                    continue
                dt, df = tf._checkDFvsDT(
                    dt=(float(parameters['dt'])*u.ms).to(u.s).value,
                    df=(float(parameters['df'])*u.kHz).to(u.Hz).value
                )
                beamConfigs.append(
                    _TFBeamConfig(
                        timeRes=dt,
                        freqRes=df,
                        durationSec=digibeams[db]['duration'],
                        nSubBands=len(digibeams[db]['subbandList'])
                    )
                )
        
        tf._beamConfigs = beamConfigs
        return tf
# ============================================================= #
# ============================================================= #


# ============================================================= #
# ------------------------- RAWConfig ------------------------- #
# ============================================================= #
class RAWConfig(_BackendConfig):
    """
    """

    def __init__(self, **kwargs):
        super().__init__(backend='raw', **kwargs)


    # --------------------------------------------------------- #
    # --------------------- Getter/Setter --------------------- #
    @property
    def volume(self):
        """
        """
        return


    # --------------------------------------------------------- #
    # ------------------------ Methods ------------------------ #
    @classmethod
    @accepts(type, (Parset, str))
    def fromParset(cls, parset):
        """
        """
        if isinstance(parset, str):
            parset = Parset(parset)

        return RAWConfig()
# ============================================================= #
# ============================================================= #


# ============================================================= #
# ---------------------- PulsarFoldConfig --------------------- #
# ============================================================= #
@doc('UnDySPuTeD Pulsar-FOLD mode observation configuration.', 'pulsar_fold')
class PulsarFoldConfig(_BackendConfig):
    """
    """

    def __init__(self, **kwargs):
        super().__init__(backend='pulsar_fold', **kwargs)


    # --------------------------------------------------------- #
    # --------------------- Getter/Setter --------------------- #
    @property
    def volume(self):
        """
        """
        duration -= 60 # burning time at start
        nchan=192


        nbit = 32
        tfold = float(extract_psr_param(parameters, '--TFOLD=')[1])
        npol = extract_psr_param(parameters, '--ONLYI')
        nbin = float(extract_psr_param(parameters, '--NBINS=')[1])
        if(npol[0]): #(if(string == "--ONLYI"))
            npol = 1
        else:
            npol = 4
        size = (float(duration)/tfold ) * nchan * npol * nbit * nbin / 8 # Bytes
        return


    # --------------------------------------------------------- #
    # ------------------------ Methods ------------------------ #
    @classmethod
    @accepts(type, (Parset, str))
    def fromParset(cls, parset):
        """
        """
        if isinstance(parset, str):
            parset = Parset(parset)

        return PulsarFoldConfig()
# ============================================================= #
# ============================================================= #


# ============================================================= #
# ---------------------- PulsarFoldConfig --------------------- #
# ============================================================= #
class PulsarWaveConfig(_BackendConfig):
    """
    """

    def __init__(self, **kwargs):
        super().__init__(backend='pulsar_waveolaf', **kwargs)


    # --------------------------------------------------------- #
    # --------------------- Getter/Setter --------------------- #
    @property
    def volume(self):
        """
        """
        return


    # --------------------------------------------------------- #
    # ------------------------ Methods ------------------------ #
    @classmethod
    @accepts(type, (Parset, str))
    def fromParset(cls, parset):
        """
        """
        if isinstance(parset, str):
            parset = Parset(parset)

        return PulsarWaveConfig()
# ============================================================= #
# ============================================================= #


# ============================================================= #
# --------------------- PulsarSingleConfig -------------------- #
# ============================================================= #
class PulsarSingleConfig(_BackendConfig):
    """
    """

    def __init__(self, **kwargs):
        super().__init__(backend='pulsar_single', **kwargs)


    # --------------------------------------------------------- #
    # --------------------- Getter/Setter --------------------- #
    @property
    def volume(self):
        """
        """
        return


    # --------------------------------------------------------- #
    # ------------------------ Methods ------------------------ #
    @classmethod
    @accepts(type, (Parset, str))
    def fromParset(cls, parset):
        """
        """
        if isinstance(parset, str):
            parset = Parset(parset)

        return PulsarSingleConfig()
# ============================================================= #
# ============================================================= #


backendClasses = {
    'nickel': NICKELConfig,
    #'raw': RAWConfig,
    'tf': TFConfig,
    'bst': BSTConfig,
    # 'sst': '',
    # 'xst': '',
    #'pulsar_fold': PulsarFoldConfig,
    #'pulsar_waveolaf': PulsarWaveConfig,
    #'pulsar_single': PulsarSingleConfig
}


# ============================================================= #
# ------------------------- ObsConfig ------------------------- #
# ============================================================= #
class ObsConfig(object):
    """ Main observation configuration class.
    """

    def __init__(self):
        for key in backendProperties:
            setattr(self, key, 0*u.Mibyte)


    @property
    def volume(self):
        """
        """
        volumes = {}
        for key in backendProperties.keys():
            volumes[key] = getattr(self, key).volume
        return volumes


    @classmethod
    @accepts(type, (Parset, str))
    def fromParset(cls, parset):
        """
        """
        if isinstance(parset, str):
            parset = Parset(parset)

        dv = ObsConfig()
        for key in backendProperties.keys():
            setattr(dv, key, backendClasses[key].fromParset(parset))
        return dv


    # @classmethod
    # @accepts(type, list)
    # def fromParsetList(cls, parsetList):
    #     """
    #     """
    #     ...
# ============================================================= #
# ============================================================= #

