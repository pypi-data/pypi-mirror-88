from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def get_points(self) -> int:
		"""[SOURce<HW>]:CORRection:CSET:DATA:POWer:POINts \n
		Queries the number of frequency/level values in the selected table. \n
			:return: points: integer Range: 0 to 10000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:CSET:DATA:POWer:POINts?')
		return Conversions.str_to_int(response)

	def get_value(self) -> List[float]:
		"""[SOURce<HW>]:CORRection:CSET:DATA:POWer \n
		Enters the level values to the table selected with [:SOURce<hw>]:CORRection:CSET[:SELect]. \n
			:return: power: Power#1[, Power#2, ...] String of values with default unit dB. *RST: 0
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce<HwInstance>:CORRection:CSET:DATA:POWer?')
		return response

	def set_value(self, power: List[float]) -> None:
		"""[SOURce<HW>]:CORRection:CSET:DATA:POWer \n
		Enters the level values to the table selected with [:SOURce<hw>]:CORRection:CSET[:SELect]. \n
			:param power: Power#1[, Power#2, ...] String of values with default unit dB. *RST: 0
		"""
		param = Conversions.list_to_csv_str(power)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:CSET:DATA:POWer {param}')
