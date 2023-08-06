from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sv:
	"""Sv commands group definition. 258 total commands, 9 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sv", core, parent)

	def clone(self) -> 'Sv':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sv(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def beidou(self):
		"""beidou commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_beidou'):
			from .Sv_.Beidou import Beidou
			self._beidou = Beidou(self._core, self._base)
		return self._beidou

	@property
	def galileo(self):
		"""galileo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_galileo'):
			from .Sv_.Galileo import Galileo
			self._galileo = Galileo(self._core, self._base)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_glonass'):
			from .Sv_.Glonass import Glonass
			self._glonass = Glonass(self._core, self._base)
		return self._glonass

	@property
	def gps(self):
		"""gps commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gps'):
			from .Sv_.Gps import Gps
			self._gps = Gps(self._core, self._base)
		return self._gps

	@property
	def importPy(self):
		"""importPy commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_importPy'):
			from .Sv_.ImportPy import ImportPy
			self._importPy = ImportPy(self._core, self._base)
		return self._importPy

	@property
	def navic(self):
		"""navic commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_navic'):
			from .Sv_.Navic import Navic
			self._navic = Navic(self._core, self._base)
		return self._navic

	@property
	def qzss(self):
		"""qzss commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_qzss'):
			from .Sv_.Qzss import Qzss
			self._qzss = Qzss(self._core, self._base)
		return self._qzss

	@property
	def sbas(self):
		"""sbas commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sbas'):
			from .Sv_.Sbas import Sbas
			self._sbas = Sbas(self._core, self._base)
		return self._sbas

	@property
	def selection(self):
		"""selection commands group. 10 Sub-classes, 1 commands."""
		if not hasattr(self, '_selection'):
			from .Sv_.Selection import Selection
			self._selection = Selection(self._core, self._base)
		return self._selection
