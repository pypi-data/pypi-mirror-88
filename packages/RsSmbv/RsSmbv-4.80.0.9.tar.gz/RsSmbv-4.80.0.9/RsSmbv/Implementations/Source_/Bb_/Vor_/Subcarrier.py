from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Subcarrier:
	"""Subcarrier commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("subcarrier", core, parent)

	def get_depth(self) -> float:
		"""[SOURce<HW>]:[BB]:VOR:SUBCarrier:DEPTh \n
		Sets the AM modulation depth of the FM carrier. \n
			:return: depth: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:SUBCarrier:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""[SOURce<HW>]:[BB]:VOR:SUBCarrier:DEPTh \n
		Sets the AM modulation depth of the FM carrier. \n
			:param depth: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:SUBCarrier:DEPTh {param}')

	def get_frequency(self) -> float:
		"""[SOURce<HW>]:[BB]:VOR:SUBCarrier:[FREQuency] \n
		Sets the frequency of the FM carrier. \n
			:return: frequency: float Range: 5E3 to 15E3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:SUBCarrier:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""[SOURce<HW>]:[BB]:VOR:SUBCarrier:[FREQuency] \n
		Sets the frequency of the FM carrier. \n
			:param frequency: float Range: 5E3 to 15E3
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:SUBCarrier:FREQuency {param}')
