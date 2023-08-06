from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpower:
	"""Dpower commands group definition. 4 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpower", core, parent)

	def clone(self) -> 'Dpower':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dpower(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mpart(self):
		"""mpart commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_mpart'):
			from .Dpower_.Mpart import Mpart
			self._mpart = Mpart(self._core, self._base)
		return self._mpart

	@property
	def preamble(self):
		"""preamble commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_preamble'):
			from .Dpower_.Preamble import Preamble
			self._preamble = Preamble(self._core, self._base)
		return self._preamble
