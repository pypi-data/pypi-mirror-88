from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ephemeris:
	"""Ephemeris commands group definition. 43 total commands, 27 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ephemeris", core, parent)

	def clone(self) -> 'Ephemeris':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ephemeris(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def aodo(self):
		"""aodo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aodo'):
			from .Ephemeris_.Aodo import Aodo
			self._aodo = Aodo(self._core, self._base)
		return self._aodo

	@property
	def asFlag(self):
		"""asFlag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_asFlag'):
			from .Ephemeris_.AsFlag import AsFlag
			self._asFlag = AsFlag(self._core, self._base)
		return self._asFlag

	@property
	def cic(self):
		"""cic commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_cic'):
			from .Ephemeris_.Cic import Cic
			self._cic = Cic(self._core, self._base)
		return self._cic

	@property
	def cis(self):
		"""cis commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_cis'):
			from .Ephemeris_.Cis import Cis
			self._cis = Cis(self._core, self._base)
		return self._cis

	@property
	def cltMmode(self):
		"""cltMmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cltMmode'):
			from .Ephemeris_.CltMmode import CltMmode
			self._cltMmode = CltMmode(self._core, self._base)
		return self._cltMmode

	@property
	def crc(self):
		"""crc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_crc'):
			from .Ephemeris_.Crc import Crc
			self._crc = Crc(self._core, self._base)
		return self._crc

	@property
	def crs(self):
		"""crs commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_crs'):
			from .Ephemeris_.Crs import Crs
			self._crs = Crs(self._core, self._base)
		return self._crs

	@property
	def cuc(self):
		"""cuc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_cuc'):
			from .Ephemeris_.Cuc import Cuc
			self._cuc = Cuc(self._core, self._base)
		return self._cuc

	@property
	def cus(self):
		"""cus commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_cus'):
			from .Ephemeris_.Cus import Cus
			self._cus = Cus(self._core, self._base)
		return self._cus

	@property
	def eccentricity(self):
		"""eccentricity commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_eccentricity'):
			from .Ephemeris_.Eccentricity import Eccentricity
			self._eccentricity = Eccentricity(self._core, self._base)
		return self._eccentricity

	@property
	def fiFlag(self):
		"""fiFlag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fiFlag'):
			from .Ephemeris_.FiFlag import FiFlag
			self._fiFlag = FiFlag(self._core, self._base)
		return self._fiFlag

	@property
	def health(self):
		"""health commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_health'):
			from .Ephemeris_.Health import Health
			self._health = Health(self._core, self._base)
		return self._health

	@property
	def idot(self):
		"""idot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_idot'):
			from .Ephemeris_.Idot import Idot
			self._idot = Idot(self._core, self._base)
		return self._idot

	@property
	def iodc(self):
		"""iodc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iodc'):
			from .Ephemeris_.Iodc import Iodc
			self._iodc = Iodc(self._core, self._base)
		return self._iodc

	@property
	def iode(self):
		"""iode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iode'):
			from .Ephemeris_.Iode import Iode
			self._iode = Iode(self._core, self._base)
		return self._iode

	@property
	def izero(self):
		"""izero commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_izero'):
			from .Ephemeris_.Izero import Izero
			self._izero = Izero(self._core, self._base)
		return self._izero

	@property
	def ltpdata(self):
		"""ltpdata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ltpdata'):
			from .Ephemeris_.Ltpdata import Ltpdata
			self._ltpdata = Ltpdata(self._core, self._base)
		return self._ltpdata

	@property
	def mzero(self):
		"""mzero commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_mzero'):
			from .Ephemeris_.Mzero import Mzero
			self._mzero = Mzero(self._core, self._base)
		return self._mzero

	@property
	def ndelta(self):
		"""ndelta commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndelta'):
			from .Ephemeris_.Ndelta import Ndelta
			self._ndelta = Ndelta(self._core, self._base)
		return self._ndelta

	@property
	def odot(self):
		"""odot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_odot'):
			from .Ephemeris_.Odot import Odot
			self._odot = Odot(self._core, self._base)
		return self._odot

	@property
	def omega(self):
		"""omega commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_omega'):
			from .Ephemeris_.Omega import Omega
			self._omega = Omega(self._core, self._base)
		return self._omega

	@property
	def ozero(self):
		"""ozero commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ozero'):
			from .Ephemeris_.Ozero import Ozero
			self._ozero = Ozero(self._core, self._base)
		return self._ozero

	@property
	def sf1Reserved(self):
		"""sf1Reserved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sf1Reserved'):
			from .Ephemeris_.Sf1Reserved import Sf1Reserved
			self._sf1Reserved = Sf1Reserved(self._core, self._base)
		return self._sf1Reserved

	@property
	def sqra(self):
		"""sqra commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_sqra'):
			from .Ephemeris_.Sqra import Sqra
			self._sqra = Sqra(self._core, self._base)
		return self._sqra

	@property
	def svConfig(self):
		"""svConfig commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_svConfig'):
			from .Ephemeris_.SvConfig import SvConfig
			self._svConfig = SvConfig(self._core, self._base)
		return self._svConfig

	@property
	def toe(self):
		"""toe commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_toe'):
			from .Ephemeris_.Toe import Toe
			self._toe = Toe(self._core, self._base)
		return self._toe

	@property
	def ura(self):
		"""ura commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ura'):
			from .Ephemeris_.Ura import Ura
			self._ura = Ura(self._core, self._base)
		return self._ura
