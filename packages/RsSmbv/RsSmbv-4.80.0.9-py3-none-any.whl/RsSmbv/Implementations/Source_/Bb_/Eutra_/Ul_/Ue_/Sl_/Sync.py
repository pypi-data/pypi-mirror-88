from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sync:
	"""Sync commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sync", core, parent)

	def clone(self) -> 'Sync':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sync(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def inCoverage(self):
		"""inCoverage commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_inCoverage'):
			from .Sync_.InCoverage import InCoverage
			self._inCoverage = InCoverage(self._core, self._base)
		return self._inCoverage

	@property
	def offsetInd(self):
		"""offsetInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offsetInd'):
			from .Sync_.OffsetInd import OffsetInd
			self._offsetInd = OffsetInd(self._core, self._base)
		return self._offsetInd

	@property
	def slssId(self):
		"""slssId commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slssId'):
			from .Sync_.SlssId import SlssId
			self._slssId = SlssId(self._core, self._base)
		return self._slssId

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Sync_.State import State
			self._state = State(self._core, self._base)
		return self._state
