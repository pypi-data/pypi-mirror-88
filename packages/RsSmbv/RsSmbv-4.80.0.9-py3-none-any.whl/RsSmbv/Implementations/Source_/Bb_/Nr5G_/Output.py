from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 53 total commands, 5 Sub-groups, 5 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Output':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Output(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def bbConf(self):
		"""bbConf commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_bbConf'):
			from .Output_.BbConf import BbConf
			self._bbConf = BbConf(self._core, self._base)
		return self._bbConf

	@property
	def cfReduction(self):
		"""cfReduction commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_cfReduction'):
			from .Output_.CfReduction import CfReduction
			self._cfReduction = CfReduction(self._core, self._base)
		return self._cfReduction

	@property
	def power(self):
		"""power commands group. 8 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Output_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def ssoc(self):
		"""ssoc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssoc'):
			from .Output_.Ssoc import Ssoc
			self._ssoc = Ssoc(self._core, self._base)
		return self._ssoc

	@property
	def tdWind(self):
		"""tdWind commands group. 12 Sub-classes, 0 commands."""
		if not hasattr(self, '_tdWind'):
			from .Output_.TdWind import TdWind
			self._tdWind = TdWind(self._core, self._base)
		return self._tdWind

	def get_clevel(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CLEVel \n
		Sets the limit for level clipping. \n
			:return: clipping_level: integer Range: 1 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CLEVel?')
		return Conversions.str_to_int(response)

	def set_clevel(self, clipping_level: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CLEVel \n
		Sets the limit for level clipping. \n
			:param clipping_level: integer Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(clipping_level)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CLEVel {param}')

	# noinspection PyTypeChecker
	def get_cmode(self) -> enums.ClipMode:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CMODe \n
		Sets the method for level clipping. \n
			:return: clipping_mode: VECTor| SCALar
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ClipMode)

	def set_cmode(self, clipping_mode: enums.ClipMode) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CMODe \n
		Sets the method for level clipping. \n
			:param clipping_mode: VECTor| SCALar
		"""
		param = Conversions.enum_scalar_to_str(clipping_mode, enums.ClipMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CMODe {param}')

	# noinspection PyTypeChecker
	def get_fmode(self) -> enums.FilterMode:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:FMODe \n
		Defines if and how the filter is applied, on the whole channel bandwidth or on the individual BWPs separately. \n
			:return: filter_bwp: CBW| BWP| OFF| FAST| 2| 1| 0| USER OFF = 'Off' CBW|0 = 'Channel BW' BWP|1 = 'Per BWP' FAST|2 = 'Fast' USER = 'User'
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:FMODe?')
		return Conversions.str_to_scalar_enum(response, enums.FilterMode)

	def set_fmode(self, filter_bwp: enums.FilterMode) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:FMODe \n
		Defines if and how the filter is applied, on the whole channel bandwidth or on the individual BWPs separately. \n
			:param filter_bwp: CBW| BWP| OFF| FAST| 2| 1| 0| USER OFF = 'Off' CBW|0 = 'Channel BW' BWP|1 = 'Per BWP' FAST|2 = 'Fast' USER = 'User'
		"""
		param = Conversions.enum_scalar_to_str(filter_bwp, enums.FilterMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:FMODe {param}')

	# noinspection PyTypeChecker
	def get_samr_mode(self) -> enums.SampRateModeRange:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:SAMRmode \n
		Sets the sample rate mode. \n
			:return: samp_rate_mode: MIN| FFT
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:SAMRmode?')
		return Conversions.str_to_scalar_enum(response, enums.SampRateModeRange)

	def set_samr_mode(self, samp_rate_mode: enums.SampRateModeRange) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:SAMRmode \n
		Sets the sample rate mode. \n
			:param samp_rate_mode: MIN| FFT
		"""
		param = Conversions.enum_scalar_to_str(samp_rate_mode, enums.SampRateModeRange)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:SAMRmode {param}')

	def get_seq_len(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:SEQLen \n
		Sets the sequence length of the signal in number of frames. \n
			:return: seq_len: integer Range: 1 to depends on settings
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:SEQLen?')
		return Conversions.str_to_int(response)

	def set_seq_len(self, seq_len: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:SEQLen \n
		Sets the sequence length of the signal in number of frames. \n
			:param seq_len: integer Range: 1 to depends on settings
		"""
		param = Conversions.decimal_value_to_str(seq_len)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:SEQLen {param}')
