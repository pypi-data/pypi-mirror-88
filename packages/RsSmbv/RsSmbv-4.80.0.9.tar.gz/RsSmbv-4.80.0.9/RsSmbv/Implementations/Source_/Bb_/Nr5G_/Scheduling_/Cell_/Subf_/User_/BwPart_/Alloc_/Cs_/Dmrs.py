from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmrs:
	"""Dmrs commands group definition. 4 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dmrs", core, parent)

	def clone(self) -> 'Dmrs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dmrs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def scram(self):
		"""scram commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_scram'):
			from .Dmrs_.Scram import Scram
			self._scram = Scram(self._core, self._base)
		return self._scram

	@property
	def space(self):
		"""space commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_space'):
			from .Dmrs_.Space import Space
			self._space = Space(self._core, self._base)
		return self._space
