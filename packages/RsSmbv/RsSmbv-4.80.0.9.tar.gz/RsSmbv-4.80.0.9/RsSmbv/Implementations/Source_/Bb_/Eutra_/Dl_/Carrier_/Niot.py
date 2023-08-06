from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Niot:
	"""Niot commands group definition. 12 total commands, 12 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("niot", core, parent)

	def clone(self) -> 'Niot':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Niot(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cell(self):
		"""cell commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cell'):
			from .Niot_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	@property
	def cidGroup(self):
		"""cidGroup commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cidGroup'):
			from .Niot_.CidGroup import CidGroup
			self._cidGroup = CidGroup(self._core, self._base)
		return self._cidGroup

	@property
	def crsseq(self):
		"""crsseq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crsseq'):
			from .Niot_.Crsseq import Crsseq
			self._crsseq = Crsseq(self._core, self._base)
		return self._crsseq

	@property
	def dfreq(self):
		"""dfreq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfreq'):
			from .Niot_.Dfreq import Dfreq
			self._dfreq = Dfreq(self._core, self._base)
		return self._dfreq

	@property
	def gbrbIdx(self):
		"""gbrbIdx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gbrbIdx'):
			from .Niot_.GbrbIdx import GbrbIdx
			self._gbrbIdx = GbrbIdx(self._core, self._base)
		return self._gbrbIdx

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Niot_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def nvsf(self):
		"""nvsf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nvsf'):
			from .Niot_.Nvsf import Nvsf
			self._nvsf = Nvsf(self._core, self._base)
		return self._nvsf

	@property
	def rbIdx(self):
		"""rbIdx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbIdx'):
			from .Niot_.RbIdx import RbIdx
			self._rbIdx = RbIdx(self._core, self._base)
		return self._rbIdx

	@property
	def sf(self):
		"""sf commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sf'):
			from .Niot_.Sf import Sf
			self._sf = Sf(self._core, self._base)
		return self._sf

	@property
	def sfall(self):
		"""sfall commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfall'):
			from .Niot_.Sfall import Sfall
			self._sfall = Sfall(self._core, self._base)
		return self._sfall

	@property
	def sfnn(self):
		"""sfnn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfnn'):
			from .Niot_.Sfnn import Sfnn
			self._sfnn = Sfnn(self._core, self._base)
		return self._sfnn

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Niot_.State import State
			self._state = State(self._core, self._base)
		return self._state
