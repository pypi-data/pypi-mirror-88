from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Receiver:
	"""Receiver commands group definition. 77 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("receiver", core, parent)

	def clone(self) -> 'Receiver':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Receiver(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def v(self):
		"""v commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_v'):
			from .Receiver_.V import V
			self._v = V(self._core, self._base)
		return self._v
