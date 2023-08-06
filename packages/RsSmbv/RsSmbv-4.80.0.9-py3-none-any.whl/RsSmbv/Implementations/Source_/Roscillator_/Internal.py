from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Internal:
	"""Internal commands group definition. 2 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("internal", core, parent)

	def clone(self) -> 'Internal':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Internal(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def adjust(self):
		"""adjust commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_adjust'):
			from .Internal_.Adjust import Adjust
			self._adjust = Adjust(self._core, self._base)
		return self._adjust
