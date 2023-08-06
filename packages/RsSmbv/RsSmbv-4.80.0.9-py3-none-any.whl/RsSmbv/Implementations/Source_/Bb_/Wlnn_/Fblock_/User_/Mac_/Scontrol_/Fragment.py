from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fragment:
	"""Fragment commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fragment", core, parent)

	def clone(self) -> 'Fragment':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fragment(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def increment(self):
		"""increment commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_increment'):
			from .Fragment_.Increment import Increment
			self._increment = Increment(self._core, self._base)
		return self._increment

	@property
	def start(self):
		"""start commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_start'):
			from .Fragment_.Start import Start
			self._start = Start(self._core, self._base)
		return self._start
