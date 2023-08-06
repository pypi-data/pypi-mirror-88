from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frc:
	"""Frc commands group definition. 10 total commands, 10 Sub-groups, 0 group commands"""

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
	def alResunits(self):
		"""alResunits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alResunits'):
			from .Frc_.AlResunits import AlResunits
			self._alResunits = AlResunits(self._core, self._base)
		return self._alResunits

	@property
	def bpresUnit(self):
		"""bpresUnit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpresUnit'):
			from .Frc_.BpresUnit import BpresUnit
			self._bpresUnit = BpresUnit(self._core, self._base)
		return self._bpresUnit

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Frc_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def nnPrep(self):
		"""nnPrep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nnPrep'):
			from .Frc_.NnPrep import NnPrep
			self._nnPrep = NnPrep(self._core, self._base)
		return self._nnPrep

	@property
	def nosCarriers(self):
		"""nosCarriers commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nosCarriers'):
			from .Frc_.NosCarriers import NosCarriers
			self._nosCarriers = NosCarriers(self._core, self._base)
		return self._nosCarriers

	@property
	def paSize(self):
		"""paSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paSize'):
			from .Frc_.PaSize import PaSize
			self._paSize = PaSize(self._core, self._base)
		return self._paSize

	@property
	def scSpacing(self):
		"""scSpacing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scSpacing'):
			from .Frc_.ScSpacing import ScSpacing
			self._scSpacing = ScSpacing(self._core, self._base)
		return self._scSpacing

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Frc_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tbssIndex(self):
		"""tbssIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbssIndex'):
			from .Frc_.TbssIndex import TbssIndex
			self._tbssIndex = TbssIndex(self._core, self._base)
		return self._tbssIndex

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Frc_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy
