from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccoding:
	"""Ccoding commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

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
	def isf(self):
		"""isf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_isf'):
			from .Ccoding_.Isf import Isf
			self._isf = Isf(self._core, self._base)
		return self._isf

	@property
	def nsf(self):
		"""nsf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsf'):
			from .Ccoding_.Nsf import Nsf
			self._nsf = Nsf(self._core, self._base)
		return self._nsf

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Ccoding_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tbsi(self):
		"""tbsi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbsi'):
			from .Ccoding_.Tbsi import Tbsi
			self._tbsi = Tbsi(self._core, self._base)
		return self._tbsi

	@property
	def tbSize(self):
		"""tbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbSize'):
			from .Ccoding_.TbSize import TbSize
			self._tbSize = TbSize(self._core, self._base)
		return self._tbSize
