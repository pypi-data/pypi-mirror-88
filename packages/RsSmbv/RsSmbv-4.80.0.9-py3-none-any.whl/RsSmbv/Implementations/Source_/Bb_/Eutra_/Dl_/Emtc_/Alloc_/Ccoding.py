from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccoding:
	"""Ccoding commands group definition. 9 total commands, 9 Sub-groups, 0 group commands"""

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
	def mib(self):
		"""mib commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mib'):
			from .Ccoding_.Mib import Mib
			self._mib = Mib(self._core, self._base)
		return self._mib

	@property
	def mspare(self):
		"""mspare commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mspare'):
			from .Ccoding_.Mspare import Mspare
			self._mspare = Mspare(self._core, self._base)
		return self._mspare

	@property
	def rsib(self):
		"""rsib commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rsib'):
			from .Ccoding_.Rsib import Rsib
			self._rsib = Rsib(self._core, self._base)
		return self._rsib

	@property
	def sib(self):
		"""sib commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sib'):
			from .Ccoding_.Sib import Sib
			self._sib = Sib(self._core, self._base)
		return self._sib

	@property
	def soffset(self):
		"""soffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_soffset'):
			from .Ccoding_.Soffset import Soffset
			self._soffset = Soffset(self._core, self._base)
		return self._soffset

	@property
	def srPeriod(self):
		"""srPeriod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srPeriod'):
			from .Ccoding_.SrPeriod import SrPeriod
			self._srPeriod = SrPeriod(self._core, self._base)
		return self._srPeriod

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
