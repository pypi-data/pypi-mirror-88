from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Niot:
	"""Niot commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("niot", core, parent)

	# noinspection PyTypeChecker
	def get_config(self) -> enums.EutraNbMimoConf:
		"""[SOURce<HW>]:BB:EUTRa:DL:MIMO:NIOT:CONFig \n
		Set the number of transmit antennas used for the simulated NB-IoT system. \n
			:return: nbiot_mimo_conf: TX2| TX1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MIMO:NIOT:CONFig?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbMimoConf)

	def set_config(self, nbiot_mimo_conf: enums.EutraNbMimoConf) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MIMO:NIOT:CONFig \n
		Set the number of transmit antennas used for the simulated NB-IoT system. \n
			:param nbiot_mimo_conf: TX2| TX1
		"""
		param = Conversions.enum_scalar_to_str(nbiot_mimo_conf, enums.EutraNbMimoConf)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MIMO:NIOT:CONFig {param}')
