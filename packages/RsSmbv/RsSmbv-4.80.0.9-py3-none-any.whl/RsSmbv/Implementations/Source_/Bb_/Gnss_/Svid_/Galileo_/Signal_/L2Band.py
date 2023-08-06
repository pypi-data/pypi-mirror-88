from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L2Band:
	"""L2Band commands group definition. 10 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("l2Band", core, parent)

	def clone(self) -> 'L2Band':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L2Band(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def e6S(self):
		"""e6S commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_e6S'):
			from .L2Band_.E6S import E6S
			self._e6S = E6S(self._core, self._base)
		return self._e6S
