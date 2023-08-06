from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Atmospheric:
	"""Atmospheric commands group definition. 48 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("atmospheric", core, parent)

	def clone(self) -> 'Atmospheric':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Atmospheric(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def beidou(self):
		"""beidou commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_beidou'):
			from .Atmospheric_.Beidou import Beidou
			self._beidou = Beidou(self._core, self._base)
		return self._beidou

	@property
	def galileo(self):
		"""galileo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_galileo'):
			from .Atmospheric_.Galileo import Galileo
			self._galileo = Galileo(self._core, self._base)
		return self._galileo

	@property
	def gps(self):
		"""gps commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gps'):
			from .Atmospheric_.Gps import Gps
			self._gps = Gps(self._core, self._base)
		return self._gps

	@property
	def ionospheric(self):
		"""ionospheric commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_ionospheric'):
			from .Atmospheric_.Ionospheric import Ionospheric
			self._ionospheric = Ionospheric(self._core, self._base)
		return self._ionospheric

	@property
	def navic(self):
		"""navic commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_navic'):
			from .Atmospheric_.Navic import Navic
			self._navic = Navic(self._core, self._base)
		return self._navic

	@property
	def qzss(self):
		"""qzss commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_qzss'):
			from .Atmospheric_.Qzss import Qzss
			self._qzss = Qzss(self._core, self._base)
		return self._qzss

	@property
	def tropospheric(self):
		"""tropospheric commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tropospheric'):
			from .Atmospheric_.Tropospheric import Tropospheric
			self._tropospheric = Tropospheric(self._core, self._base)
		return self._tropospheric
