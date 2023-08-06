from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def get_points(self) -> int:
		"""[SOURce<HW>]:LIST:FREQuency:POINts \n
		Queries the number (points) of frequency entries in the seleced list. \n
			:return: points: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:FREQuency:POINts?')
		return Conversions.str_to_int(response)

	def get_value(self) -> List[float]:
		"""[SOURce<HW>]:LIST:FREQuency \n
		Enters the frequency values in the selected list. \n
			:return: frequency: Frequency#1{, Frequency#2, ...} | block data You can either enter the data as a list of numbers, or as binary block data. The list of numbers can be of any length, with the list entries separated by commas. In binary block format, 8 (4) bytes are always interpreted as a floating-point number with double accuracy. See also :​FORMat[:​DATA]. Range: 300 kHz to RFmax (depends on the installed options)
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce<HwInstance>:LIST:FREQuency?')
		return response

	def set_value(self, frequency: List[float]) -> None:
		"""[SOURce<HW>]:LIST:FREQuency \n
		Enters the frequency values in the selected list. \n
			:param frequency: Frequency#1{, Frequency#2, ...} | block data You can either enter the data as a list of numbers, or as binary block data. The list of numbers can be of any length, with the list entries separated by commas. In binary block format, 8 (4) bytes are always interpreted as a floating-point number with double accuracy. See also :​FORMat[:​DATA]. Range: 300 kHz to RFmax (depends on the installed options)
		"""
		param = Conversions.list_to_csv_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:LIST:FREQuency {param}')
