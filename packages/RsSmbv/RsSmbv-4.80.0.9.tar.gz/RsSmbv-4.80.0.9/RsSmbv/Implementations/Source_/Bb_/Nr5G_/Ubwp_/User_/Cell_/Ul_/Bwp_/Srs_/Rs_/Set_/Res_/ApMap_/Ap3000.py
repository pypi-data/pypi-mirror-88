from ...............Internal.Core import Core
from ...............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ap3000:
	"""Ap3000 commands group definition. 4 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ap3000", core, parent)

	def clone(self) -> 'Ap3000':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ap3000(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def row(self):
		"""row commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_row'):
			from .Ap3000_.Row import Row
			self._row = Row(self._core, self._base)
		return self._row
