from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal.RepeatedCapability import RepeatedCapability
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Space:
	"""Space commands group definition. 2 total commands, 2 Sub-groups, 0 group commands
	Repeated Capability: SpaceIx, default value after init: SpaceIx.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("space", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_spaceIx_get', 'repcap_spaceIx_set', repcap.SpaceIx.Nr0)

	def clone(self) -> 'Space':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Space(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_spaceIx_set(self, enum_value: repcap.SpaceIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to SpaceIx.Default
		Default value after init: SpaceIx.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_spaceIx_get(self) -> repcap.SpaceIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def aggLevel(self):
		"""aggLevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aggLevel'):
			from .Space_.AggLevel import AggLevel
			self._aggLevel = AggLevel(self._core, self._base)
		return self._aggLevel

	@property
	def maxCandidate(self):
		"""maxCandidate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_maxCandidate'):
			from .Space_.MaxCandidate import MaxCandidate
			self._maxCandidate = MaxCandidate(self._core, self._base)
		return self._maxCandidate
