from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Am:
	"""Am commands group definition. 7 total commands, 5 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("am", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Am':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Am(self._core, self._base.parent)
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
	def depth(self):
		"""depth commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_depth'):
			from .Am_.Depth import Depth
			self._depth = Depth(self._core, self._base)
		return self._depth

	@property
	def deviation(self):
		"""deviation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_deviation'):
			from .Am_.Deviation import Deviation
			self._deviation = Deviation(self._core, self._base)
		return self._deviation

	@property
	def sensitivity(self):
		"""sensitivity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sensitivity'):
			from .Am_.Sensitivity import Sensitivity
			self._sensitivity = Sensitivity(self._core, self._base)
		return self._sensitivity

	@property
	def source(self):
		"""source commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_source'):
			from .Am_.Source import Source
			self._source = Source(self._core, self._base)
		return self._source

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Am_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def get_ratio(self) -> float:
		"""[SOURce<HW>]:AM:RATio \n
		Sets the deviation ratio (path#2 to path#1) in percent. \n
			:return: ratio: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AM:RATio?')
		return Conversions.str_to_float(response)

	def set_ratio(self, ratio: float) -> None:
		"""[SOURce<HW>]:AM:RATio \n
		Sets the deviation ratio (path#2 to path#1) in percent. \n
			:param ratio: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(ratio)
		self._core.io.write(f'SOURce<HwInstance>:AM:RATio {param}')
