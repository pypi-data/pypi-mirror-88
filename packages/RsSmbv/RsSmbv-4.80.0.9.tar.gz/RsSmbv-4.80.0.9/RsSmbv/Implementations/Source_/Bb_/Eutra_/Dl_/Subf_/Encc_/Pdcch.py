from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pdcch:
	"""Pdcch commands group definition. 83 total commands, 14 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pdcch", core, parent)

	def clone(self) -> 'Pdcch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pdcch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def alRegs(self):
		"""alRegs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alRegs'):
			from .Pdcch_.AlRegs import AlRegs
			self._alRegs = AlRegs(self._core, self._base)
		return self._alRegs

	@property
	def avcces(self):
		"""avcces commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_avcces'):
			from .Pdcch_.Avcces import Avcces
			self._avcces = Avcces(self._core, self._base)
		return self._avcces

	@property
	def avRegs(self):
		"""avRegs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_avRegs'):
			from .Pdcch_.AvRegs import AvRegs
			self._avRegs = AvRegs(self._core, self._base)
		return self._avRegs

	@property
	def bits(self):
		"""bits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bits'):
			from .Pdcch_.Bits import Bits
			self._bits = Bits(self._core, self._base)
		return self._bits

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Pdcch_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dcRegs(self):
		"""dcRegs commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_dcRegs'):
			from .Pdcch_.DcRegs import DcRegs
			self._dcRegs = DcRegs(self._core, self._base)
		return self._dcRegs

	@property
	def dregs(self):
		"""dregs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dregs'):
			from .Pdcch_.Dregs import Dregs
			self._dregs = Dregs(self._core, self._base)
		return self._dregs

	@property
	def dselect(self):
		"""dselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselect'):
			from .Pdcch_.Dselect import Dselect
			self._dselect = Dselect(self._core, self._base)
		return self._dselect

	@property
	def extc(self):
		"""extc commands group. 9 Sub-classes, 2 commands."""
		if not hasattr(self, '_extc'):
			from .Pdcch_.Extc import Extc
			self._extc = Extc(self._core, self._base)
		return self._extc

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .Pdcch_.FormatPy import FormatPy
			self._formatPy = FormatPy(self._core, self._base)
		return self._formatPy

	@property
	def noPdcchs(self):
		"""noPdcchs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noPdcchs'):
			from .Pdcch_.NoPdcchs import NoPdcchs
			self._noPdcchs = NoPdcchs(self._core, self._base)
		return self._noPdcchs

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pdcch_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Pdcch_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def scrambling(self):
		"""scrambling commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambling'):
			from .Pdcch_.Scrambling import Scrambling
			self._scrambling = Scrambling(self._core, self._base)
		return self._scrambling
