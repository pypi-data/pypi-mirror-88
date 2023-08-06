from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class C2K:
	"""C2K commands group definition. 143 total commands, 13 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("c2K", core, parent)

	def clone(self) -> 'C2K':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = C2K(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bstation(self):
		"""bstation commands group. 9 Sub-classes, 1 commands."""
		if not hasattr(self, '_bstation'):
			from .C2K_.Bstation import Bstation
			self._bstation = Bstation(self._core, self._base)
		return self._bstation

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .C2K_.Clipping import Clipping
			self._clipping = Clipping(self._core, self._base)
		return self._clipping

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .C2K_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def copy(self):
		"""copy commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_copy'):
			from .C2K_.Copy import Copy
			self._copy = Copy(self._core, self._base)
		return self._copy

	@property
	def crate(self):
		"""crate commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_crate'):
			from .C2K_.Crate import Crate
			self._crate = Crate(self._core, self._base)
		return self._crate

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .C2K_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def iqswap(self):
		"""iqswap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqswap'):
			from .C2K_.Iqswap import Iqswap
			self._iqswap = Iqswap(self._core, self._base)
		return self._iqswap

	@property
	def mstation(self):
		"""mstation commands group. 8 Sub-classes, 1 commands."""
		if not hasattr(self, '_mstation'):
			from .C2K_.Mstation import Mstation
			self._mstation = Mstation(self._core, self._base)
		return self._mstation

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .C2K_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def pparameter(self):
		"""pparameter commands group. 5 Sub-classes, 2 commands."""
		if not hasattr(self, '_pparameter'):
			from .C2K_.Pparameter import Pparameter
			self._pparameter = Pparameter(self._core, self._base)
		return self._pparameter

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .C2K_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def trigger(self):
		"""trigger commands group. 4 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .C2K_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .C2K_.Waveform import Waveform
			self._waveform = Waveform(self._core, self._base)
		return self._waveform

	# noinspection PyTypeChecker
	def get_link(self) -> enums.LinkDir:
		"""[SOURce<HW>]:BB:C2K:LINK \n
		The command defines the transmission direction. The signal either corresponds to that of a base station (FORWard | DOWN)
		or that of a mobile station (REVerse | UP) . \n
			:return: link: DOWN| UP| FORWard| REVerse
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:LINK?')
		return Conversions.str_to_scalar_enum(response, enums.LinkDir)

	def set_link(self, link: enums.LinkDir) -> None:
		"""[SOURce<HW>]:BB:C2K:LINK \n
		The command defines the transmission direction. The signal either corresponds to that of a base station (FORWard | DOWN)
		or that of a mobile station (REVerse | UP) . \n
			:param link: DOWN| UP| FORWard| REVerse
		"""
		param = Conversions.enum_scalar_to_str(link, enums.LinkDir)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:LINK {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:C2K:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.C2K.state. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:C2K:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.C2K.state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:C2K:PRESet')

	def get_slength(self) -> int:
		"""[SOURce<HW>]:BB:C2K:SLENgth \n
		Sets the sequence length of the arbitrary waveform component of the CDMA2000 signal in the number of frames. \n
			:return: slength: integer Range: 1 to max
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""[SOURce<HW>]:BB:C2K:SLENgth \n
		Sets the sequence length of the arbitrary waveform component of the CDMA2000 signal in the number of frames. \n
			:param slength: integer Range: 1 to max
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:SLENgth {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:C2K:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:C2K:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:STATe {param}')

	def get_version(self) -> str:
		"""[SOURce]:BB:C2K:VERSion \n
		The command queries the version of the CDMA standard underlying the definitions. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SOURce:BB:C2K:VERSion?')
		return trim_str_response(response)
