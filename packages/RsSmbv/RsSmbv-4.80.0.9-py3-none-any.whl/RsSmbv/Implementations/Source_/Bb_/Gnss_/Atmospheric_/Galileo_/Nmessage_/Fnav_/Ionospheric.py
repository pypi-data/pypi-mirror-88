from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ionospheric:
	"""Ionospheric commands group definition. 3 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ionospheric", core, parent)

	def clone(self) -> 'Ionospheric':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ionospheric(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ai(self):
		"""ai commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai'):
			from .Ionospheric_.Ai import Ai
			self._ai = Ai(self._core, self._base)
		return self._ai

	@property
	def sf(self):
		"""sf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sf'):
			from .Ionospheric_.Sf import Sf
			self._sf = Sf(self._core, self._base)
		return self._sf
