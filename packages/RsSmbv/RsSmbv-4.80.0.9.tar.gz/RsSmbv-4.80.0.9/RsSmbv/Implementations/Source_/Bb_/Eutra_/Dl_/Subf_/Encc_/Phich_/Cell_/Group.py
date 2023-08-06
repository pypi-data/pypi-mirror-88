from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Group:
	"""Group commands group definition. 1 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: Group, default value after init: Group.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("group", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_group_get', 'repcap_group_set', repcap.Group.Nr1)

	def clone(self) -> 'Group':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Group(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_group_set(self, enum_value: repcap.Group) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Group.Default
		Default value after init: Group.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_group_get(self) -> repcap.Group:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def item(self):
		"""item commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_item'):
			from .Group_.Item import Item
			self._item = Item(self._core, self._base)
		return self._item
