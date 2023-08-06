from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdGeneration:
	"""AdGeneration commands group definition. 88 total commands, 10 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("adGeneration", core, parent)

	def clone(self) -> 'AdGeneration':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AdGeneration(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def acquisition(self):
		"""acquisition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acquisition'):
			from .AdGeneration_.Acquisition import Acquisition
			self._acquisition = Acquisition(self._core, self._base)
		return self._acquisition

	@property
	def almanac(self):
		"""almanac commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_almanac'):
			from .AdGeneration_.Almanac import Almanac
			self._almanac = Almanac(self._core, self._base)
		return self._almanac

	@property
	def beidou(self):
		"""beidou commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_beidou'):
			from .AdGeneration_.Beidou import Beidou
			self._beidou = Beidou(self._core, self._base)
		return self._beidou

	@property
	def galileo(self):
		"""galileo commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_galileo'):
			from .AdGeneration_.Galileo import Galileo
			self._galileo = Galileo(self._core, self._base)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_glonass'):
			from .AdGeneration_.Glonass import Glonass
			self._glonass = Glonass(self._core, self._base)
		return self._glonass

	@property
	def gps(self):
		"""gps commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_gps'):
			from .AdGeneration_.Gps import Gps
			self._gps = Gps(self._core, self._base)
		return self._gps

	@property
	def ionospheric(self):
		"""ionospheric commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ionospheric'):
			from .AdGeneration_.Ionospheric import Ionospheric
			self._ionospheric = Ionospheric(self._core, self._base)
		return self._ionospheric

	@property
	def navigation(self):
		"""navigation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_navigation'):
			from .AdGeneration_.Navigation import Navigation
			self._navigation = Navigation(self._core, self._base)
		return self._navigation

	@property
	def qzss(self):
		"""qzss commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_qzss'):
			from .AdGeneration_.Qzss import Qzss
			self._qzss = Qzss(self._core, self._base)
		return self._qzss

	@property
	def utc(self):
		"""utc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_utc'):
			from .AdGeneration_.Utc import Utc
			self._utc = Utc(self._core, self._base)
		return self._utc

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.Hybrid:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:MODE \n
		Defines the type of assistance data to be loaded. \n
			:return: mode: GPS| GALileo| GLONass| NAVic| QZSS| SBAS| BEIDou
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ADGeneration:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.Hybrid)

	def set_mode(self, mode: enums.Hybrid) -> None:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:MODE \n
		Defines the type of assistance data to be loaded. \n
			:param mode: GPS| GALileo| GLONass| NAVic| QZSS| SBAS| BEIDou
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.Hybrid)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:MODE {param}')
