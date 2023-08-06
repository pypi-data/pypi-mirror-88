from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frc:
	"""Frc commands group definition. 33 total commands, 17 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frc", core, parent)

	def clone(self) -> 'Frc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def channel(self):
		"""channel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channel'):
			from .Frc_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	@property
	def crate(self):
		"""crate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crate'):
			from .Frc_.Crate import Crate
			self._crate = Crate(self._core, self._base)
		return self._crate

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Frc_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def derror(self):
		"""derror commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_derror'):
			from .Frc_.Derror import Derror
			self._derror = Derror(self._core, self._base)
		return self._derror

	@property
	def dtx(self):
		"""dtx commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtx'):
			from .Frc_.Dtx import Dtx
			self._dtx = Dtx(self._core, self._base)
		return self._dtx

	@property
	def harq(self):
		"""harq commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Frc_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq

	@property
	def hprocesses(self):
		"""hprocesses commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hprocesses'):
			from .Frc_.Hprocesses import Hprocesses
			self._hprocesses = Hprocesses(self._core, self._base)
		return self._hprocesses

	@property
	def mibrate(self):
		"""mibrate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mibrate'):
			from .Frc_.Mibrate import Mibrate
			self._mibrate = Mibrate(self._core, self._base)
		return self._mibrate

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Frc_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def orate(self):
		"""orate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_orate'):
			from .Frc_.Orate import Orate
			self._orate = Orate(self._core, self._base)
		return self._orate

	@property
	def paybits(self):
		"""paybits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paybits'):
			from .Frc_.Paybits import Paybits
			self._paybits = Paybits(self._core, self._base)
		return self._paybits

	@property
	def pcCodes(self):
		"""pcCodes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcCodes'):
			from .Frc_.PcCodes import PcCodes
			self._pcCodes = PcCodes(self._core, self._base)
		return self._pcCodes

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Frc_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tbs(self):
		"""tbs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tbs'):
			from .Frc_.Tbs import Tbs
			self._tbs = Tbs(self._core, self._base)
		return self._tbs

	@property
	def ttiBits(self):
		"""ttiBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiBits'):
			from .Frc_.TtiBits import TtiBits
			self._ttiBits = TtiBits(self._core, self._base)
		return self._ttiBits

	@property
	def ttiedch(self):
		"""ttiedch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiedch'):
			from .Frc_.Ttiedch import Ttiedch
			self._ttiedch = Ttiedch(self._core, self._base)
		return self._ttiedch

	@property
	def ueCategory(self):
		"""ueCategory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueCategory'):
			from .Frc_.UeCategory import UeCategory
			self._ueCategory = UeCategory(self._core, self._base)
		return self._ueCategory
