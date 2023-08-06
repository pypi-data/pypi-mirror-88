from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bit:
	"""Bit commands group definition. 5 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: BitNumber, default value after init: BitNumber.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bit", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_bitNumber_get', 'repcap_bitNumber_set', repcap.BitNumber.Nr0)

	def clone(self) -> 'Bit':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bit(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_bitNumber_set(self, enum_value: repcap.BitNumber) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to BitNumber.Default
		Default value after init: BitNumber.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_bitNumber_get(self) -> repcap.BitNumber:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def condition(self):
		"""condition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_condition'):
			from .Bit_.Condition import Condition
			self._condition = Condition(self._core, self._base)
		return self._condition

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Bit_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def ntransition(self):
		"""ntransition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntransition'):
			from .Bit_.Ntransition import Ntransition
			self._ntransition = Ntransition(self._core, self._base)
		return self._ntransition

	@property
	def ptransition(self):
		"""ptransition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptransition'):
			from .Bit_.Ptransition import Ptransition
			self._ptransition = Ptransition(self._core, self._base)
		return self._ptransition

	@property
	def event(self):
		"""event commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_event'):
			from .Bit_.Event import Event
			self._event = Event(self._core, self._base)
		return self._event
