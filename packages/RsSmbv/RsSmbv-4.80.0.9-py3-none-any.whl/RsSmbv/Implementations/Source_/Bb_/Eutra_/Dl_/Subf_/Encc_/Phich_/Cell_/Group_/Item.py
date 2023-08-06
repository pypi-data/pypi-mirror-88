from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal.RepeatedCapability import RepeatedCapability
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Item:
	"""Item commands group definition. 1 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: UserItem, default value after init: UserItem.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("item", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_userItem_get', 'repcap_userItem_set', repcap.UserItem.Nr1)

	def clone(self) -> 'Item':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Item(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_userItem_set(self, enum_value: repcap.UserItem) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to UserItem.Default
		Default value after init: UserItem.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_userItem_get(self) -> repcap.UserItem:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def pow(self):
		"""pow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pow'):
			from .Item_.Pow import Pow
			self._pow = Pow(self._core, self._base)
		return self._pow
