from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mimo:
	"""Mimo commands group definition. 7 total commands, 2 Sub-groups, 2 group commands"""

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
	def apm(self):
		"""apm commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_apm'):
			from .Mimo_.Apm import Apm
			self._apm = Apm(self._core, self._base)
		return self._apm

	@property
	def niot(self):
		"""niot commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_niot'):
			from .Mimo_.Niot import Niot
			self._niot = Niot(self._core, self._base)
		return self._niot

	# noinspection PyTypeChecker
	def get_antenna(self) -> enums.EutraSimAnt:
		"""[SOURce<HW>]:BB:EUTRa:DL:MIMO:ANTenna \n
		(For backwards compatibility only) Sets the simulated antenna. The simulated antenna is determined by the remote commands
		of the mapping table. \n
			:return: antenna: ANT1| ANT2| ANT3| ANT4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MIMO:ANTenna?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSimAnt)

	def set_antenna(self, antenna: enums.EutraSimAnt) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MIMO:ANTenna \n
		(For backwards compatibility only) Sets the simulated antenna. The simulated antenna is determined by the remote commands
		of the mapping table. \n
			:param antenna: ANT1| ANT2| ANT3| ANT4
		"""
		param = Conversions.enum_scalar_to_str(antenna, enums.EutraSimAnt)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MIMO:ANTenna {param}')

	# noinspection PyTypeChecker
	def get_configuration(self) -> enums.EutraGlobMimoConf:
		"""[SOURce<HW>]:BB:EUTRa:DL:MIMO:CONFiguration \n
		Sets the global MIMO configuration. \n
			:return: configuration: TX1| TX2| TX4| SIBF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MIMO:CONFiguration?')
		return Conversions.str_to_scalar_enum(response, enums.EutraGlobMimoConf)

	def set_configuration(self, configuration: enums.EutraGlobMimoConf) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MIMO:CONFiguration \n
		Sets the global MIMO configuration. \n
			:param configuration: TX1| TX2| TX4| SIBF
		"""
		param = Conversions.enum_scalar_to_str(configuration, enums.EutraGlobMimoConf)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MIMO:CONFiguration {param}')
