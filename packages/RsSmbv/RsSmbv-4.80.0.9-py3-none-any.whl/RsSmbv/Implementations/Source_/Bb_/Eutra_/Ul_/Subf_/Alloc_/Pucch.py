from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pucch:
	"""Pucch commands group definition. 20 total commands, 15 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pucch", core, parent)

	def clone(self) -> 'Pucch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pucch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Pucch_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def cqi(self):
		"""cqi commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_cqi'):
			from .Pucch_.Cqi import Cqi
			self._cqi = Cqi(self._core, self._base)
		return self._cqi

	@property
	def cycShift(self):
		"""cycShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cycShift'):
			from .Pucch_.CycShift import CycShift
			self._cycShift = CycShift(self._core, self._base)
		return self._cycShift

	@property
	def dmr1(self):
		"""dmr1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmr1'):
			from .Pucch_.Dmr1 import Dmr1
			self._dmr1 = Dmr1(self._core, self._base)
		return self._dmr1

	@property
	def dmr2(self):
		"""dmr2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmr2'):
			from .Pucch_.Dmr2 import Dmr2
			self._dmr2 = Dmr2(self._core, self._base)
		return self._dmr2

	@property
	def harq(self):
		"""harq commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Pucch_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq

	@property
	def mrb(self):
		"""mrb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mrb'):
			from .Pucch_.Mrb import Mrb
			self._mrb = Mrb(self._core, self._base)
		return self._mrb

	@property
	def napUsed(self):
		"""napUsed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_napUsed'):
			from .Pucch_.NapUsed import NapUsed
			self._napUsed = NapUsed(self._core, self._base)
		return self._napUsed

	@property
	def noc(self):
		"""noc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noc'):
			from .Pucch_.Noc import Noc
			self._noc = Noc(self._core, self._base)
		return self._noc

	@property
	def npar(self):
		"""npar commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_npar'):
			from .Pucch_.Npar import Npar
			self._npar = Npar(self._core, self._base)
		return self._npar

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .Pucch_.PhysBits import PhysBits
			self._physBits = PhysBits(self._core, self._base)
		return self._physBits

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Pucch_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def rbCount(self):
		"""rbCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbCount'):
			from .Pucch_.RbCount import RbCount
			self._rbCount = RbCount(self._core, self._base)
		return self._rbCount

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Pucch_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .Pucch_.FormatPy import FormatPy
			self._formatPy = FormatPy(self._core, self._base)
		return self._formatPy
