from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ul:
	"""Ul commands group definition. 18 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ul", core, parent)

	def clone(self) -> 'Ul':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ul(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def afSeq(self):
		"""afSeq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_afSeq'):
			from .Ul_.AfSeq import AfSeq
			self._afSeq = AfSeq(self._core, self._base)
		return self._afSeq

	@property
	def cell(self):
		"""cell commands group. 6 Sub-classes, 2 commands."""
		if not hasattr(self, '_cell'):
			from .Ul_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	@property
	def indi(self):
		"""indi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_indi'):
			from .Ul_.Indi import Indi
			self._indi = Indi(self._core, self._base)
		return self._indi

	@property
	def nhtrans(self):
		"""nhtrans commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nhtrans'):
			from .Ul_.Nhtrans import Nhtrans
			self._nhtrans = Nhtrans(self._core, self._base)
		return self._nhtrans
