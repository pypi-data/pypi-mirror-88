from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Carrier:
	"""Carrier commands group definition. 10 total commands, 7 Sub-groups, 3 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("carrier", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Carrier':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Carrier(self._core, self._base.parent)
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
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Carrier_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Carrier_.Delay import Delay
			self._delay = Delay(self._core, self._base)
		return self._delay

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_file'):
			from .Carrier_.File import File
			self._file = File(self._core, self._base)
		return self._file

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Carrier_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def phase(self):
		"""phase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phase'):
			from .Carrier_.Phase import Phase
			self._phase = Phase(self._core, self._base)
		return self._phase

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Carrier_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Carrier_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def get_count(self) -> int:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier:COUNt \n
		Sets the number of carriers in the ARB multi-carrier waveform. \n
			:return: count: integer Range: 1 to 512
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, count: int) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier:COUNt \n
		Sets the number of carriers in the ARB multi-carrier waveform. \n
			:param count: integer Range: 1 to 512
		"""
		param = Conversions.decimal_value_to_str(count)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier:COUNt {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ArbMultCarrSpacMode:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier:MODE \n
		The command sets the carrier frequency mode. \n
			:return: mode: EQUidistant| ARBitrary
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ArbMultCarrSpacMode)

	def set_mode(self, mode: enums.ArbMultCarrSpacMode) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier:MODE \n
		The command sets the carrier frequency mode. \n
			:param mode: EQUidistant| ARBitrary
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ArbMultCarrSpacMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier:MODE {param}')

	def get_spacing(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier:SPACing \n
		Sets the frequency spacing between adjacent carriers of the multi-carrier waveform (see 'Defining the Carrier Frequency')
		. \n
			:return: spacing: float Range: 0.0 to depends on the installed options, e.g. 120E6, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier:SPACing?')
		return Conversions.str_to_float(response)

	def set_spacing(self, spacing: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier:SPACing \n
		Sets the frequency spacing between adjacent carriers of the multi-carrier waveform (see 'Defining the Carrier Frequency')
		. \n
			:param spacing: float Range: 0.0 to depends on the installed options, e.g. 120E6, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(spacing)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier:SPACing {param}')
