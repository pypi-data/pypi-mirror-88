from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L5Band:
	"""L5Band commands group definition. 8 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("l5Band", core, parent)

	def clone(self) -> 'L5Band':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L5Band(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def sps(self):
		"""sps commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_sps'):
			from .L5Band_.Sps import Sps
			self._sps = Sps(self._core, self._base)
		return self._sps
