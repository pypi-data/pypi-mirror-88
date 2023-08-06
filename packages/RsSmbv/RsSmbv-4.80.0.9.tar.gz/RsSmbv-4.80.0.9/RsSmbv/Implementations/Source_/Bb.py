from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bb:
	"""Bb commands group definition. 7793 total commands, 36 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bb", core, parent)

	def clone(self) -> 'Bb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bb(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def arbitrary(self):
		"""arbitrary commands group. 9 Sub-classes, 2 commands."""
		if not hasattr(self, '_arbitrary'):
			from .Bb_.Arbitrary import Arbitrary
			self._arbitrary = Arbitrary(self._core, self._base)
		return self._arbitrary

	@property
	def btooth(self):
		"""btooth commands group. 16 Sub-classes, 17 commands."""
		if not hasattr(self, '_btooth'):
			from .Bb_.Btooth import Btooth
			self._btooth = Btooth(self._core, self._base)
		return self._btooth

	@property
	def c2K(self):
		"""c2K commands group. 13 Sub-classes, 5 commands."""
		if not hasattr(self, '_c2K'):
			from .Bb_.C2K import C2K
			self._c2K = C2K(self._core, self._base)
		return self._c2K

	@property
	def coder(self):
		"""coder commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coder'):
			from .Bb_.Coder import Coder
			self._coder = Coder(self._core, self._base)
		return self._coder

	@property
	def dab(self):
		"""dab commands group. 11 Sub-classes, 7 commands."""
		if not hasattr(self, '_dab'):
			from .Bb_.Dab import Dab
			self._dab = Dab(self._core, self._base)
		return self._dab

	@property
	def dm(self):
		"""dm commands group. 18 Sub-classes, 7 commands."""
		if not hasattr(self, '_dm'):
			from .Bb_.Dm import Dm
			self._dm = Dm(self._core, self._base)
		return self._dm

	@property
	def dme(self):
		"""dme commands group. 12 Sub-classes, 15 commands."""
		if not hasattr(self, '_dme'):
			from .Bb_.Dme import Dme
			self._dme = Dme(self._core, self._base)
		return self._dme

	@property
	def eutra(self):
		"""eutra commands group. 16 Sub-classes, 7 commands."""
		if not hasattr(self, '_eutra'):
			from .Bb_.Eutra import Eutra
			self._eutra = Eutra(self._core, self._base)
		return self._eutra

	@property
	def evdo(self):
		"""evdo commands group. 13 Sub-classes, 8 commands."""
		if not hasattr(self, '_evdo'):
			from .Bb_.Evdo import Evdo
			self._evdo = Evdo(self._core, self._base)
		return self._evdo

	@property
	def gbas(self):
		"""gbas commands group. 8 Sub-classes, 9 commands."""
		if not hasattr(self, '_gbas'):
			from .Bb_.Gbas import Gbas
			self._gbas = Gbas(self._core, self._base)
		return self._gbas

	@property
	def graphics(self):
		"""graphics commands group. 2 Sub-classes, 6 commands."""
		if not hasattr(self, '_graphics'):
			from .Bb_.Graphics import Graphics
			self._graphics = Graphics(self._core, self._base)
		return self._graphics

	@property
	def gsm(self):
		"""gsm commands group. 17 Sub-classes, 7 commands."""
		if not hasattr(self, '_gsm'):
			from .Bb_.Gsm import Gsm
			self._gsm = Gsm(self._core, self._base)
		return self._gsm

	@property
	def huwb(self):
		"""huwb commands group. 11 Sub-classes, 11 commands."""
		if not hasattr(self, '_huwb'):
			from .Bb_.Huwb import Huwb
			self._huwb = Huwb(self._core, self._base)
		return self._huwb

	@property
	def impairment(self):
		"""impairment commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_impairment'):
			from .Bb_.Impairment import Impairment
			self._impairment = Impairment(self._core, self._base)
		return self._impairment

	@property
	def info(self):
		"""info commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Bb_.Info import Info
			self._info = Info(self._core, self._base)
		return self._info

	@property
	def lora(self):
		"""lora commands group. 7 Sub-classes, 6 commands."""
		if not hasattr(self, '_lora'):
			from .Bb_.Lora import Lora
			self._lora = Lora(self._core, self._base)
		return self._lora

	@property
	def mccw(self):
		"""mccw commands group. 5 Sub-classes, 2 commands."""
		if not hasattr(self, '_mccw'):
			from .Bb_.Mccw import Mccw
			self._mccw = Mccw(self._core, self._base)
		return self._mccw

	@property
	def nfc(self):
		"""nfc commands group. 10 Sub-classes, 12 commands."""
		if not hasattr(self, '_nfc'):
			from .Bb_.Nfc import Nfc
			self._nfc = Nfc(self._core, self._base)
		return self._nfc

	@property
	def nr5G(self):
		"""nr5G commands group. 24 Sub-classes, 6 commands."""
		if not hasattr(self, '_nr5G'):
			from .Bb_.Nr5G import Nr5G
			self._nr5G = Nr5G(self._core, self._base)
		return self._nr5G

	@property
	def ofdm(self):
		"""ofdm commands group. 17 Sub-classes, 14 commands."""
		if not hasattr(self, '_ofdm'):
			from .Bb_.Ofdm import Ofdm
			self._ofdm = Ofdm(self._core, self._base)
		return self._ofdm

	@property
	def path(self):
		"""path commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_path'):
			from .Bb_.Path import Path
			self._path = Path(self._core, self._base)
		return self._path

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Bb_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def pramp(self):
		"""pramp commands group. 5 Sub-classes, 2 commands."""
		if not hasattr(self, '_pramp'):
			from .Bb_.Pramp import Pramp
			self._pramp = Pramp(self._core, self._base)
		return self._pramp

	@property
	def progress(self):
		"""progress commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_progress'):
			from .Bb_.Progress import Progress
			self._progress = Progress(self._core, self._base)
		return self._progress

	@property
	def sirius(self):
		"""sirius commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_sirius'):
			from .Bb_.Sirius import Sirius
			self._sirius = Sirius(self._core, self._base)
		return self._sirius

	@property
	def stereo(self):
		"""stereo commands group. 7 Sub-classes, 5 commands."""
		if not hasattr(self, '_stereo'):
			from .Bb_.Stereo import Stereo
			self._stereo = Stereo(self._core, self._base)
		return self._stereo

	@property
	def tdscdma(self):
		"""tdscdma commands group. 12 Sub-classes, 6 commands."""
		if not hasattr(self, '_tdscdma'):
			from .Bb_.Tdscdma import Tdscdma
			self._tdscdma = Tdscdma(self._core, self._base)
		return self._tdscdma

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Bb_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def vor(self):
		"""vor commands group. 10 Sub-classes, 3 commands."""
		if not hasattr(self, '_vor'):
			from .Bb_.Vor import Vor
			self._vor = Vor(self._core, self._base)
		return self._vor

	@property
	def w3Gpp(self):
		"""w3Gpp commands group. 13 Sub-classes, 5 commands."""
		if not hasattr(self, '_w3Gpp'):
			from .Bb_.W3Gpp import W3Gpp
			self._w3Gpp = W3Gpp(self._core, self._base)
		return self._w3Gpp

	@property
	def wlan(self):
		"""wlan commands group. 13 Sub-classes, 9 commands."""
		if not hasattr(self, '_wlan'):
			from .Bb_.Wlan import Wlan
			self._wlan = Wlan(self._core, self._base)
		return self._wlan

	@property
	def wlnn(self):
		"""wlnn commands group. 10 Sub-classes, 8 commands."""
		if not hasattr(self, '_wlnn'):
			from .Bb_.Wlnn import Wlnn
			self._wlnn = Wlnn(self._core, self._base)
		return self._wlnn

	@property
	def xmradio(self):
		"""xmradio commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_xmradio'):
			from .Bb_.Xmradio import Xmradio
			self._xmradio = Xmradio(self._core, self._base)
		return self._xmradio

	@property
	def ils(self):
		"""ils commands group. 7 Sub-classes, 3 commands."""
		if not hasattr(self, '_ils'):
			from .Bb_.Ils import Ils
			self._ils = Ils(self._core, self._base)
		return self._ils

	@property
	def gnpr(self):
		"""gnpr commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gnpr'):
			from .Bb_.Gnpr import Gnpr
			self._gnpr = Gnpr(self._core, self._base)
		return self._gnpr

	@property
	def gnss(self):
		"""gnss commands group. 25 Sub-classes, 7 commands."""
		if not hasattr(self, '_gnss'):
			from .Bb_.Gnss import Gnss
			self._gnss = Gnss(self._core, self._base)
		return self._gnss

	def get_cfactor(self) -> float:
		"""[SOURce<HW>]:BB:CFACtor \n
		Queries the crest factor of the baseband signal. \n
			:return: cfactor: float Range: 0 to 100, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:CFACtor?')
		return Conversions.str_to_float(response)

	def get_foffset(self) -> float:
		"""[SOURce<HW>]:BB:FOFFset \n
		Sets a frequency offset for the internal/external baseband signal. The offset affects the generated baseband signal. \n
			:return: fo_ffset: float Range: depends on the installed options , Unit: Hz E.g. -60 MHz to +60 MHz (base unit)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:FOFFset?')
		return Conversions.str_to_float(response)

	def set_foffset(self, fo_ffset: float) -> None:
		"""[SOURce<HW>]:BB:FOFFset \n
		Sets a frequency offset for the internal/external baseband signal. The offset affects the generated baseband signal. \n
			:param fo_ffset: float Range: depends on the installed options , Unit: Hz E.g. -60 MHz to +60 MHz (base unit)
		"""
		param = Conversions.decimal_value_to_str(fo_ffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:FOFFset {param}')

	# noinspection PyTypeChecker
	def get_iq_gain(self) -> enums.IqGain:
		"""[SOURce<HW>]:BB:IQGain \n
		Optimizes the modulation of the I/Q modulator for a subset of measurement requirement. \n
			:return: ipartq_gain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:IQGain?')
		return Conversions.str_to_scalar_enum(response, enums.IqGain)

	def set_iq_gain(self, ipartq_gain: enums.IqGain) -> None:
		"""[SOURce<HW>]:BB:IQGain \n
		Optimizes the modulation of the I/Q modulator for a subset of measurement requirement. \n
			:param ipartq_gain: DBM4| DBM2| DB0| DB2| DB4| DB8| DB6 Dynamic range of 16 dB divided into 2 dB steps. DB0|DB2|DB4|DB6|DB8 Activates the specified gain of 0 dB, +2 dB, +4 dB, +6 dB, +8 dB DBM2|DBM4 Activates the specified gain of -2 dB, -4 dB
		"""
		param = Conversions.enum_scalar_to_str(ipartq_gain, enums.IqGain)
		self._core.io.write(f'SOURce<HwInstance>:BB:IQGain {param}')

	def get_pgain(self) -> float:
		"""[SOURce<HW>]:BB:PGAin \n
		No command help available \n
			:return: pgain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PGAin?')
		return Conversions.str_to_float(response)

	def set_pgain(self, pgain: float) -> None:
		"""[SOURce<HW>]:BB:PGAin \n
		No command help available \n
			:param pgain: No help available
		"""
		param = Conversions.decimal_value_to_str(pgain)
		self._core.io.write(f'SOURce<HwInstance>:BB:PGAin {param}')

	def get_poffset(self) -> float:
		"""[SOURce<HW>]:BB:POFFset \n
		Sets the relative phase offset for the selected baseband signal. \n
			:return: poffset: float Range: 0 to 359.9, Unit: DEG
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:POFFset?')
		return Conversions.str_to_float(response)

	def set_poffset(self, poffset: float) -> None:
		"""[SOURce<HW>]:BB:POFFset \n
		Sets the relative phase offset for the selected baseband signal. \n
			:param poffset: float Range: 0 to 359.9, Unit: DEG
		"""
		param = Conversions.decimal_value_to_str(poffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:POFFset {param}')

	# noinspection PyTypeChecker
	def get_route(self) -> enums.PathUniCodBbin:
		"""[SOURce<HW>]:BB:ROUTe \n
		Selects the signal route for the internal/external baseband signal. \n
			:return: route: A
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ROUTe?')
		return Conversions.str_to_scalar_enum(response, enums.PathUniCodBbin)

	def set_route(self, route: enums.PathUniCodBbin) -> None:
		"""[SOURce<HW>]:BB:ROUTe \n
		Selects the signal route for the internal/external baseband signal. \n
			:param route: A
		"""
		param = Conversions.enum_scalar_to_str(route, enums.PathUniCodBbin)
		self._core.io.write(f'SOURce<HwInstance>:BB:ROUTe {param}')
