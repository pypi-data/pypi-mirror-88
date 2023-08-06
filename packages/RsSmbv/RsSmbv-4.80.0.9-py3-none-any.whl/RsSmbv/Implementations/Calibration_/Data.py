from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 3 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def clone(self) -> 'Data':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Data(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def factory(self):
		"""factory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_factory'):
			from .Data_.Factory import Factory
			self._factory = Factory(self._core, self._base)
		return self._factory

	@property
	def update(self):
		"""update commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_update'):
			from .Data_.Update import Update
			self._update = Update(self._core, self._base)
		return self._update
