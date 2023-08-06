from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccoding:
	"""Ccoding commands group definition. 6 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ccoding", core, parent)

	def clone(self) -> 'Ccoding':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ccoding(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def icqiOffset(self):
		"""icqiOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icqiOffset'):
			from .Ccoding_.IcqiOffset import IcqiOffset
			self._icqiOffset = IcqiOffset(self._core, self._base)
		return self._icqiOffset

	@property
	def iharqOffset(self):
		"""iharqOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iharqOffset'):
			from .Ccoding_.IharqOffset import IharqOffset
			self._iharqOffset = IharqOffset(self._core, self._base)
		return self._iharqOffset

	@property
	def iriOffset(self):
		"""iriOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iriOffset'):
			from .Ccoding_.IriOffset import IriOffset
			self._iriOffset = IriOffset(self._core, self._base)
		return self._iriOffset

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Ccoding_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def ocqiMin(self):
		"""ocqiMin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ocqiMin'):
			from .Ccoding_.OcqiMin import OcqiMin
			self._ocqiMin = OcqiMin(self._core, self._base)
		return self._ocqiMin

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Ccoding_.State import State
			self._state = State(self._core, self._base)
		return self._state
