from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ephemeris:
	"""Ephemeris commands group definition. 36 total commands, 20 Sub-groups, 0 group commands"""

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
	def idot(self):
		"""idot commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_idot'):
			from .Ephemeris_.Idot import Idot
			self._idot = Idot(self._core, self._base)
		return self._idot

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
	def l5Health(self):
		"""l5Health commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_l5Health'):
			from .Ephemeris_.L5Health import L5Health
			self._l5Health = L5Health(self._core, self._base)
		return self._l5Health

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
	def shealth(self):
		"""shealth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shealth'):
			from .Ephemeris_.Shealth import Shealth
			self._shealth = Shealth(self._core, self._base)
		return self._shealth

	@property
	def sqra(self):
		"""sqra commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_sqra'):
			from .Ephemeris_.Sqra import Sqra
			self._sqra = Sqra(self._core, self._base)
		return self._sqra

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
