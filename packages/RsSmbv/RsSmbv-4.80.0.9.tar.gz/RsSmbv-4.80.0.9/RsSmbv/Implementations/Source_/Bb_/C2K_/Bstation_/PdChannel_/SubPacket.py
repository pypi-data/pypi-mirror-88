from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubPacket:
	"""SubPacket commands group definition. 5 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: Subpacket, default value after init: Subpacket.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subPacket", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_subpacket_get', 'repcap_subpacket_set', repcap.Subpacket.Nr1)

	def clone(self) -> 'SubPacket':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SubPacket(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_subpacket_set(self, enum_value: repcap.Subpacket) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Subpacket.Default
		Default value after init: Subpacket.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_subpacket_get(self) -> repcap.Subpacket:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def id(self):
		"""id commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_id'):
			from .SubPacket_.Id import Id
			self._id = Id(self._core, self._base)
		return self._id

	@property
	def parameters(self):
		"""parameters commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_parameters'):
			from .SubPacket_.Parameters import Parameters
			self._parameters = Parameters(self._core, self._base)
		return self._parameters

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .SubPacket_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def toffset(self):
		"""toffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toffset'):
			from .SubPacket_.Toffset import Toffset
			self._toffset = Toffset(self._core, self._base)
		return self._toffset

	@property
	def wcodes(self):
		"""wcodes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wcodes'):
			from .SubPacket_.Wcodes import Wcodes
			self._wcodes = Wcodes(self._core, self._base)
		return self._wcodes
