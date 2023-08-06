from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Notch:
	"""Notch commands group definition. 8 total commands, 4 Sub-groups, 3 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("notch", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Notch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Notch(self._core, self._base.parent)
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
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Notch_.Apply import Apply
			self._apply = Apply(self._core, self._base)
		return self._apply

	@property
	def bandwidth(self):
		"""bandwidth commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_bandwidth'):
			from .Notch_.Bandwidth import Bandwidth
			self._bandwidth = Bandwidth(self._core, self._base)
		return self._bandwidth

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Notch_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Notch_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def get_clock(self) -> int:
		"""[SOURce<HW>]:BB:OFDM:NOTCh:CLOCk \n
		No command help available \n
			:return: clock_freq: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:NOTCh:CLOCk?')
		return Conversions.str_to_int(response)

	def get_count(self) -> int:
		"""[SOURce<HW>]:BB:OFDM:NOTCh:COUNt \n
		No command help available \n
			:return: num_of_notch: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:NOTCh:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, num_of_notch: int) -> None:
		"""[SOURce<HW>]:BB:OFDM:NOTCh:COUNt \n
		No command help available \n
			:param num_of_notch: No help available
		"""
		param = Conversions.decimal_value_to_str(num_of_notch)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:NOTCh:COUNt {param}')

	def get_value(self) -> bool:
		"""[SOURce<HW>]:BB:OFDM:NOTCh \n
		No command help available \n
			:return: notch_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:OFDM:NOTCh?')
		return Conversions.str_to_bool(response)

	def set_value(self, notch_state: bool) -> None:
		"""[SOURce<HW>]:BB:OFDM:NOTCh \n
		No command help available \n
			:param notch_state: No help available
		"""
		param = Conversions.bool_to_str(notch_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:NOTCh {param}')
