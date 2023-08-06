from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Phich:
	"""Phich commands group definition. 6 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("phich", core, parent)

	def clone(self) -> 'Phich':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Phich(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def anPattern(self):
		"""anPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_anPattern'):
			from .Phich_.AnPattern import AnPattern
			self._anPattern = AnPattern(self._core, self._base)
		return self._anPattern

	@property
	def cell(self):
		"""cell commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Phich_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	@property
	def pmode(self):
		"""pmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmode'):
			from .Phich_.Pmode import Pmode
			self._pmode = Pmode(self._core, self._base)
		return self._pmode

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Phich_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power
