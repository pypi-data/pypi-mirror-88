from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Marker:
	"""Marker commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("marker", core, parent)

	def get_frequency(self) -> int:
		"""[SOURce<HW>]:[ILS]:MBEacon:MARKer:FREQuency \n
		Sets the modulation frequency of the marker signal for the ILS marker beacon modulation signal. \n
			:return: frequency: 400| 1300| 3000 Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:MBEacon:MARKer:FREQuency?')
		return Conversions.str_to_int(response)

	def set_frequency(self, frequency: int) -> None:
		"""[SOURce<HW>]:[ILS]:MBEacon:MARKer:FREQuency \n
		Sets the modulation frequency of the marker signal for the ILS marker beacon modulation signal. \n
			:param frequency: 400| 1300| 3000 Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:MARKer:FREQuency {param}')
