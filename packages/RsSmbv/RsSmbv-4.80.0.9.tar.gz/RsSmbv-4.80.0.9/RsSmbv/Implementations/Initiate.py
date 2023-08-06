from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Initiate:
	"""Initiate commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("initiate", core, parent)

	def clone(self) -> 'Initiate':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Initiate(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def freqSweep(self):
		"""freqSweep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_freqSweep'):
			from .Initiate_.FreqSweep import FreqSweep
			self._freqSweep = FreqSweep(self._core, self._base)
		return self._freqSweep

	@property
	def lffSweep(self):
		"""lffSweep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lffSweep'):
			from .Initiate_.LffSweep import LffSweep
			self._lffSweep = LffSweep(self._core, self._base)
		return self._lffSweep

	@property
	def listPy(self):
		"""listPy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_listPy'):
			from .Initiate_.ListPy import ListPy
			self._listPy = ListPy(self._core, self._base)
		return self._listPy

	@property
	def psweep(self):
		"""psweep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_psweep'):
			from .Initiate_.Psweep import Psweep
			self._psweep = Psweep(self._core, self._base)
		return self._psweep

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Initiate_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power
