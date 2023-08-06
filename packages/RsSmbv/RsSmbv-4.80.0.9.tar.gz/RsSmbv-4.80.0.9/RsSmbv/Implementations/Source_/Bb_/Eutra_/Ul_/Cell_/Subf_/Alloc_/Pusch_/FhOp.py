from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FhOp:
	"""FhOp commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fhOp", core, parent)

	def clone(self) -> 'FhOp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FhOp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def iihbits(self):
		"""iihbits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iihbits'):
			from .FhOp_.Iihbits import Iihbits
			self._iihbits = Iihbits(self._core, self._base)
		return self._iihbits

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .FhOp_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .FhOp_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .FhOp_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy
