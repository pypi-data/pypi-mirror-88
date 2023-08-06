from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccoding:
	"""Ccoding commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

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
	def isbSize(self):
		"""isbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_isbSize'):
			from .Ccoding_.IsbSize import IsbSize
			self._isbSize = IsbSize(self._core, self._base)
		return self._isbSize

	@property
	def rvIndex(self):
		"""rvIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvIndex'):
			from .Ccoding_.RvIndex import RvIndex
			self._rvIndex = RvIndex(self._core, self._base)
		return self._rvIndex

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Ccoding_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tbSize(self):
		"""tbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbSize'):
			from .Ccoding_.TbSize import TbSize
			self._tbSize = TbSize(self._core, self._base)
		return self._tbSize
