from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mimo:
	"""Mimo commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mimo", core, parent)

	def clone(self) -> 'Mimo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mimo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cvpb(self):
		"""cvpb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cvpb'):
			from .Mimo_.Cvpb import Cvpb
			self._cvpb = Cvpb(self._core, self._base)
		return self._cvpb

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Mimo_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def pwPattern(self):
		"""pwPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pwPattern'):
			from .Mimo_.PwPattern import PwPattern
			self._pwPattern = PwPattern(self._core, self._base)
		return self._pwPattern

	@property
	def staPattern(self):
		"""staPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_staPattern'):
			from .Mimo_.StaPattern import StaPattern
			self._staPattern = StaPattern(self._core, self._base)
		return self._staPattern
