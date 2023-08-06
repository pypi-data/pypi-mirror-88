from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L1Band:
	"""L1Band commands group definition. 1 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("l1Band", core, parent)

	def clone(self) -> 'L1Band':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L1Band(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def e1Os(self):
		"""e1Os commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_e1Os'):
			from .L1Band_.E1Os import E1Os
			self._e1Os = E1Os(self._core, self._base)
		return self._e1Os
