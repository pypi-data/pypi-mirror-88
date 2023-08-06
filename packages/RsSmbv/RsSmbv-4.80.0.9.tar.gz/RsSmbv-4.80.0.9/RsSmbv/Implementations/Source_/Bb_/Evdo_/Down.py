from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Down:
	"""Down commands group definition. 7 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("down", core, parent)

	def clone(self) -> 'Down':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Down(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mc(self):
		"""mc commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_mc'):
			from .Down_.Mc import Mc
			self._mc = Mc(self._core, self._base)
		return self._mc
