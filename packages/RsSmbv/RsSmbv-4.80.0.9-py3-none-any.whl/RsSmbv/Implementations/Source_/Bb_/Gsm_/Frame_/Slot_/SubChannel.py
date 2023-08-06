from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SubChannel:
	"""SubChannel commands group definition. 27 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: Subchannel, default value after init: Subchannel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subChannel", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_subchannel_get', 'repcap_subchannel_set', repcap.Subchannel.Nr1)

	def clone(self) -> 'SubChannel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SubChannel(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_subchannel_set(self, enum_value: repcap.Subchannel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Subchannel.Default
		Default value after init: Subchannel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_subchannel_get(self) -> repcap.Subchannel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def user(self):
		"""user commands group. 13 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .SubChannel_.User import User
			self._user = User(self._core, self._base)
		return self._user
