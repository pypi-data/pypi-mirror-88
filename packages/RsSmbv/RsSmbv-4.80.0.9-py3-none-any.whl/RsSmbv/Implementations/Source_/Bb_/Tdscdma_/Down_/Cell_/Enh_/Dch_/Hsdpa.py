from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hsdpa:
	"""Hsdpa commands group definition. 25 total commands, 21 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hsdpa", core, parent)

	def clone(self) -> 'Hsdpa':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hsdpa(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bpayload(self):
		"""bpayload commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpayload'):
			from .Hsdpa_.Bpayload import Bpayload
			self._bpayload = Bpayload(self._core, self._base)
		return self._bpayload

	@property
	def crate(self):
		"""crate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crate'):
			from .Hsdpa_.Crate import Crate
			self._crate = Crate(self._core, self._base)
		return self._crate

	@property
	def ctsCount(self):
		"""ctsCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctsCount'):
			from .Hsdpa_.CtsCount import CtsCount
			self._ctsCount = CtsCount(self._core, self._base)
		return self._ctsCount

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Hsdpa_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def harq(self):
		"""harq commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Hsdpa_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq

	@property
	def mibt(self):
		"""mibt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mibt'):
			from .Hsdpa_.Mibt import Mibt
			self._mibt = Mibt(self._core, self._base)
		return self._mibt

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Hsdpa_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def ncbtti(self):
		"""ncbtti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncbtti'):
			from .Hsdpa_.Ncbtti import Ncbtti
			self._ncbtti = Ncbtti(self._core, self._base)
		return self._ncbtti

	@property
	def rmc(self):
		"""rmc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmc'):
			from .Hsdpa_.Rmc import Rmc
			self._rmc = Rmc(self._core, self._base)
		return self._rmc

	@property
	def rvParameter(self):
		"""rvParameter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvParameter'):
			from .Hsdpa_.RvParameter import RvParameter
			self._rvParameter = RvParameter(self._core, self._base)
		return self._rvParameter

	@property
	def rvSequence(self):
		"""rvSequence commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvSequence'):
			from .Hsdpa_.RvSequence import RvSequence
			self._rvSequence = RvSequence(self._core, self._base)
		return self._rvSequence

	@property
	def scch(self):
		"""scch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scch'):
			from .Hsdpa_.Scch import Scch
			self._scch = Scch(self._core, self._base)
		return self._scch

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Hsdpa_.Sformat import Sformat
			self._sformat = Sformat(self._core, self._base)
		return self._sformat

	@property
	def spattern(self):
		"""spattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spattern'):
			from .Hsdpa_.Spattern import Spattern
			self._spattern = Spattern(self._core, self._base)
		return self._spattern

	@property
	def tbs(self):
		"""tbs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tbs'):
			from .Hsdpa_.Tbs import Tbs
			self._tbs = Tbs(self._core, self._base)
		return self._tbs

	@property
	def tsCount(self):
		"""tsCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsCount'):
			from .Hsdpa_.TsCount import TsCount
			self._tsCount = TsCount(self._core, self._base)
		return self._tsCount

	@property
	def ttiDistance(self):
		"""ttiDistance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttiDistance'):
			from .Hsdpa_.TtiDistance import TtiDistance
			self._ttiDistance = TtiDistance(self._core, self._base)
		return self._ttiDistance

	@property
	def ttInterval(self):
		"""ttInterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttInterval'):
			from .Hsdpa_.TtInterval import TtInterval
			self._ttInterval = TtInterval(self._core, self._base)
		return self._ttInterval

	@property
	def ueCategory(self):
		"""ueCategory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueCategory'):
			from .Hsdpa_.UeCategory import UeCategory
			self._ueCategory = UeCategory(self._core, self._base)
		return self._ueCategory

	@property
	def ueid(self):
		"""ueid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueid'):
			from .Hsdpa_.Ueid import Ueid
			self._ueid = Ueid(self._core, self._base)
		return self._ueid

	@property
	def vibSize(self):
		"""vibSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vibSize'):
			from .Hsdpa_.VibSize import VibSize
			self._vibSize = VibSize(self._core, self._base)
		return self._vibSize
