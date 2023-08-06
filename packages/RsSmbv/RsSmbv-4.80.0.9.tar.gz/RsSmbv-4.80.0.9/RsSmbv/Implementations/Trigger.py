from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 14 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	def clone(self) -> 'Trigger':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trigger(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def fpSweep(self):
		"""fpSweep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fpSweep'):
			from .Trigger_.FpSweep import FpSweep
			self._fpSweep = FpSweep(self._core, self._base)
		return self._fpSweep

	@property
	def freqSweep(self):
		"""freqSweep commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_freqSweep'):
			from .Trigger_.FreqSweep import FreqSweep
			self._freqSweep = FreqSweep(self._core, self._base)
		return self._freqSweep

	@property
	def lffSweep(self):
		"""lffSweep commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_lffSweep'):
			from .Trigger_.LffSweep import LffSweep
			self._lffSweep = LffSweep(self._core, self._base)
		return self._lffSweep

	@property
	def listPy(self):
		"""listPy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_listPy'):
			from .Trigger_.ListPy import ListPy
			self._listPy = ListPy(self._core, self._base)
		return self._listPy

	@property
	def psweep(self):
		"""psweep commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_psweep'):
			from .Trigger_.Psweep import Psweep
			self._psweep = Psweep(self._core, self._base)
		return self._psweep

	@property
	def sweep(self):
		"""sweep commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_sweep'):
			from .Trigger_.Sweep import Sweep
			self._sweep = Sweep(self._core, self._base)
		return self._sweep
