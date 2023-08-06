from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Awgn:
	"""Awgn commands group definition. 22 total commands, 5 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("awgn", core, parent)

	def clone(self) -> 'Awgn':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Awgn(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bandwidth(self):
		"""bandwidth commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_bandwidth'):
			from .Awgn_.Bandwidth import Bandwidth
			self._bandwidth = Bandwidth(self._core, self._base)
		return self._bandwidth

	@property
	def cmode(self):
		"""cmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cmode'):
			from .Awgn_.Cmode import Cmode
			self._cmode = Cmode(self._core, self._base)
		return self._cmode

	@property
	def disp(self):
		"""disp commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_disp'):
			from .Awgn_.Disp import Disp
			self._disp = Disp(self._core, self._base)
		return self._disp

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Awgn_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def power(self):
		"""power commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_power'):
			from .Awgn_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	def get_brate(self) -> float:
		"""[SOURce<HW>]:AWGN:BRATe \n
		Sets the bit rate used for calculation of bit energy to noise power ratio. Valid units are bps, kbps and mabps as well as
		b/s, kb/s and mab/s. \n
			:return: brate: float Range: 400 to depends on the installed options
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:BRATe?')
		return Conversions.str_to_float(response)

	def set_brate(self, brate: float) -> None:
		"""[SOURce<HW>]:AWGN:BRATe \n
		Sets the bit rate used for calculation of bit energy to noise power ratio. Valid units are bps, kbps and mabps as well as
		b/s, kb/s and mab/s. \n
			:param brate: float Range: 400 to depends on the installed options
		"""
		param = Conversions.decimal_value_to_str(brate)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:BRATe {param}')

	def get_cn_ratio(self) -> float:
		"""[SOURce<HW>]:AWGN:CNRatio \n
		Sets the carrier/interferer ratio. \n
			:return: cn_ratio: float Range: -50 to 45
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:CNRatio?')
		return Conversions.str_to_float(response)

	def set_cn_ratio(self, cn_ratio: float) -> None:
		"""[SOURce<HW>]:AWGN:CNRatio \n
		Sets the carrier/interferer ratio. \n
			:param cn_ratio: float Range: -50 to 45
		"""
		param = Conversions.decimal_value_to_str(cn_ratio)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:CNRatio {param}')

	def get_en_ratio(self) -> float:
		"""[SOURce<HW>]:AWGN:ENRatio \n
		Sets the ratio of bit energy to noise power density. \n
			:return: en_ratio: float Range: -50 to depends on the installed options, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:ENRatio?')
		return Conversions.str_to_float(response)

	def set_en_ratio(self, en_ratio: float) -> None:
		"""[SOURce<HW>]:AWGN:ENRatio \n
		Sets the ratio of bit energy to noise power density. \n
			:param en_ratio: float Range: -50 to depends on the installed options, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(en_ratio)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:ENRatio {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.NoisAwgnMode:
		"""[SOURce<HW>]:AWGN:MODE \n
		Determines how the interfering signal is generated. \n
			:return: mode: ONLY| ADD| CW ADD The AWGN noise signal is added to the baseband signal. ONLY The pure AWGN noise signal is modulated to the carrier. The connection to the baseband is interrupted CW The sine interfering signal is added to the baseband signal.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.NoisAwgnMode)

	def set_mode(self, mode: enums.NoisAwgnMode) -> None:
		"""[SOURce<HW>]:AWGN:MODE \n
		Determines how the interfering signal is generated. \n
			:param mode: ONLY| ADD| CW ADD The AWGN noise signal is added to the baseband signal. ONLY The pure AWGN noise signal is modulated to the carrier. The connection to the baseband is interrupted CW The sine interfering signal is added to the baseband signal.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.NoisAwgnMode)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:MODE {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:AWGN:STATe \n
		Activates or deactivates the AWGN generator. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:AWGN:STATe \n
		Activates or deactivates the AWGN generator. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:STATe {param}')
