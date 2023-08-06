from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mimo:
	"""Mimo commands group definition. 11 total commands, 8 Sub-groups, 0 group commands"""

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
	def poaAck(self):
		"""poaAck commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poaAck'):
			from .Mimo_.PoaAck import PoaAck
			self._poaAck = PoaAck(self._core, self._base)
		return self._poaAck

	@property
	def poaNack(self):
		"""poaNack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poaNack'):
			from .Mimo_.PoaNack import PoaNack
			self._poaNack = PoaNack(self._core, self._base)
		return self._poaNack

	@property
	def poca(self):
		"""poca commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poca'):
			from .Mimo_.Poca import Poca
			self._poca = Poca(self._core, self._base)
		return self._poca

	@property
	def poNack(self):
		"""poNack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poNack'):
			from .Mimo_.PoNack import PoNack
			self._poNack = PoNack(self._core, self._base)
		return self._poNack

	@property
	def ponNack(self):
		"""ponNack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ponNack'):
			from .Mimo_.PonNack import PonNack
			self._ponNack = PonNack(self._core, self._base)
		return self._ponNack

	@property
	def tti(self):
		"""tti commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tti'):
			from .Mimo_.Tti import Tti
			self._tti = Tti(self._core, self._base)
		return self._tti

	@property
	def ttiCount(self):
		"""ttiCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiCount'):
			from .Mimo_.TtiCount import TtiCount
			self._ttiCount = TtiCount(self._core, self._base)
		return self._ttiCount

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mimo_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode
