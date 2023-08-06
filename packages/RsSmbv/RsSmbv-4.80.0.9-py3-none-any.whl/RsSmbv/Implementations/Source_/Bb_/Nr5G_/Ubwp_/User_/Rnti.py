from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rnti:
	"""Rnti commands group definition. 6 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rnti", core, parent)

	def clone(self) -> 'Rnti':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rnti(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cs(self):
		"""cs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cs'):
			from .Rnti_.Cs import Cs
			self._cs = Cs(self._core, self._base)
		return self._cs

	@property
	def mcsc(self):
		"""mcsc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcsc'):
			from .Rnti_.Mcsc import Mcsc
			self._mcsc = Mcsc(self._core, self._base)
		return self._mcsc

	@property
	def ra(self):
		"""ra commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ra'):
			from .Rnti_.Ra import Ra
			self._ra = Ra(self._core, self._base)
		return self._ra

	@property
	def sfi(self):
		"""sfi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfi'):
			from .Rnti_.Sfi import Sfi
			self._sfi = Sfi(self._core, self._base)
		return self._sfi

	@property
	def spcsi(self):
		"""spcsi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spcsi'):
			from .Rnti_.Spcsi import Spcsi
			self._spcsi = Spcsi(self._core, self._base)
		return self._spcsi

	@property
	def tc(self):
		"""tc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tc'):
			from .Rnti_.Tc import Tc
			self._tc = Tc(self._core, self._base)
		return self._tc
