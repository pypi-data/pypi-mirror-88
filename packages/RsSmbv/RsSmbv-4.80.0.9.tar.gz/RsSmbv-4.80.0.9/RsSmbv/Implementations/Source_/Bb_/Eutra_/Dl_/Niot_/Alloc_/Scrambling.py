from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scrambling:
	"""Scrambling commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scrambling", core, parent)

	def clone(self) -> 'Scrambling':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Scrambling(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def legacy(self):
		"""legacy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_legacy'):
			from .Scrambling_.Legacy import Legacy
			self._legacy = Legacy(self._core, self._base)
		return self._legacy

	@property
	def srot(self):
		"""srot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srot'):
			from .Scrambling_.Srot import Srot
			self._srot = Srot(self._core, self._base)
		return self._srot

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Scrambling_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def ueid(self):
		"""ueid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueid'):
			from .Scrambling_.Ueid import Ueid
			self._ueid = Ueid(self._core, self._base)
		return self._ueid
