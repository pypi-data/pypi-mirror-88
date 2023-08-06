from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApMap:
	"""ApMap commands group definition. 5 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: AntennaPortMap, default value after init: AntennaPortMap.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apMap", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_antennaPortMap_get', 'repcap_antennaPortMap_set', repcap.AntennaPortMap.Nr0)

	def clone(self) -> 'ApMap':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ApMap(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_antennaPortMap_set(self, enum_value: repcap.AntennaPortMap) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AntennaPortMap.Default
		Default value after init: AntennaPortMap.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_antennaPortMap_get(self) -> repcap.AntennaPortMap:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def col(self):
		"""col commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_col'):
			from .ApMap_.Col import Col
			self._col = Col(self._core, self._base)
		return self._col

	@property
	def mindex(self):
		"""mindex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mindex'):
			from .ApMap_.Mindex import Mindex
			self._mindex = Mindex(self._core, self._base)
		return self._mindex
