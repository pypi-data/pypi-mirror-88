from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmrs:
	"""Dmrs commands group definition. 7 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dmrs", core, parent)

	def clone(self) -> 'Dmrs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dmrs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .Dmrs_.Length import Length
			self._length = Length(self._core, self._base)
		return self._length

	@property
	def nsid(self):
		"""nsid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsid'):
			from .Dmrs_.Nsid import Nsid
			self._nsid = Nsid(self._core, self._base)
		return self._nsid

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Dmrs_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def seqGen(self):
		"""seqGen commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_seqGen'):
			from .Dmrs_.SeqGen import SeqGen
			self._seqGen = SeqGen(self._core, self._base)
		return self._seqGen

	@property
	def seqHopping(self):
		"""seqHopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_seqHopping'):
			from .Dmrs_.SeqHopping import SeqHopping
			self._seqHopping = SeqHopping(self._core, self._base)
		return self._seqHopping

	@property
	def sltSymbols(self):
		"""sltSymbols commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sltSymbols'):
			from .Dmrs_.SltSymbols import SltSymbols
			self._sltSymbols = SltSymbols(self._core, self._base)
		return self._sltSymbols

	@property
	def apSelect(self):
		"""apSelect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apSelect'):
			from .Dmrs_.ApSelect import ApSelect
			self._apSelect = ApSelect(self._core, self._base)
		return self._apSelect
