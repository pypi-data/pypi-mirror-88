from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frc:
	"""Frc commands group definition. 8 total commands, 8 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frc", core, parent)

	def clone(self) -> 'Frc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def alrb(self):
		"""alrb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alrb'):
			from .Frc_.Alrb import Alrb
			self._alrb = Alrb(self._core, self._base)
		return self._alrb

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Frc_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def n2Dmrs(self):
		"""n2Dmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n2Dmrs'):
			from .Frc_.N2Dmrs import N2Dmrs
			self._n2Dmrs = N2Dmrs(self._core, self._base)
		return self._n2Dmrs

	@property
	def paSize(self):
		"""paSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paSize'):
			from .Frc_.PaSize import PaSize
			self._paSize = PaSize(self._core, self._base)
		return self._paSize

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Frc_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tnoBits(self):
		"""tnoBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tnoBits'):
			from .Frc_.TnoBits import TnoBits
			self._tnoBits = TnoBits(self._core, self._base)
		return self._tnoBits

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Frc_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy

	@property
	def vrbOffset(self):
		"""vrbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vrbOffset'):
			from .Frc_.VrbOffset import VrbOffset
			self._vrbOffset = VrbOffset(self._core, self._base)
		return self._vrbOffset
