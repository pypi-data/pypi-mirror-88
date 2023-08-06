from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Encc:
	"""Encc commands group definition. 96 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("encc", core, parent)

	def clone(self) -> 'Encc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Encc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def pcfich(self):
		"""pcfich commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcfich'):
			from .Encc_.Pcfich import Pcfich
			self._pcfich = Pcfich(self._core, self._base)
		return self._pcfich

	@property
	def pdcch(self):
		"""pdcch commands group. 14 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdcch'):
			from .Encc_.Pdcch import Pdcch
			self._pdcch = Pdcch(self._core, self._base)
		return self._pdcch

	@property
	def phich(self):
		"""phich commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_phich'):
			from .Encc_.Phich import Phich
			self._phich = Phich(self._core, self._base)
		return self._phich

	@property
	def precoding(self):
		"""precoding commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_precoding'):
			from .Encc_.Precoding import Precoding
			self._precoding = Precoding(self._core, self._base)
		return self._precoding

	@property
	def scrambling(self):
		"""scrambling commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambling'):
			from .Encc_.Scrambling import Scrambling
			self._scrambling = Scrambling(self._core, self._base)
		return self._scrambling

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Encc_.State import State
			self._state = State(self._core, self._base)
		return self._state
