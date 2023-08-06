from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pin:
	"""Pin commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pin", core, parent)

	def clone(self) -> 'Pin':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pin(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def max(self):
		"""max commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_max'):
			from .Pin_.Max import Max
			self._max = Max(self._core, self._base)
		return self._max

	@property
	def min(self):
		"""min commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_min'):
			from .Pin_.Min import Min
			self._min = Min(self._core, self._base)
		return self._min
