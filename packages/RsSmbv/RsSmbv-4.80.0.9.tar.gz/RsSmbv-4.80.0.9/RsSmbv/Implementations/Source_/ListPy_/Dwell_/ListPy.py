from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ListPy:
	"""ListPy commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("listPy", core, parent)

	def get_points(self) -> int:
		"""[SOURce<HW>]:LIST:DWELl:LIST:POINts \n
		Queries the number (points) of dwell time entries in the selected list. \n
			:return: points: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:DWELl:LIST:POINts?')
		return Conversions.str_to_int(response)

	def get_value(self) -> List[int]:
		"""[SOURce<HW>]:LIST:DWELl:LIST \n
		Enters the dwell time values in the selected list in µs. \n
			:return: dwell: Dwell#1{, Dwell#2, ...} | block data You can either enter the data as a list of numbers, or as binary block data. The list of numbers can be of any length, with the list entries separated by commas. In binary block format, 8 (4) bytes are always interpreted as a floating-point number with double accuracy. See also :​FORMat[:​DATA] for more details.
		"""
		response = self._core.io.query_bin_or_ascii_int_list('SOURce<HwInstance>:LIST:DWELl:LIST?')
		return response

	def set_value(self, dwell: List[int]) -> None:
		"""[SOURce<HW>]:LIST:DWELl:LIST \n
		Enters the dwell time values in the selected list in µs. \n
			:param dwell: Dwell#1{, Dwell#2, ...} | block data You can either enter the data as a list of numbers, or as binary block data. The list of numbers can be of any length, with the list entries separated by commas. In binary block format, 8 (4) bytes are always interpreted as a floating-point number with double accuracy. See also :​FORMat[:​DATA] for more details.
		"""
		param = Conversions.list_to_csv_str(dwell)
		self._core.io.write(f'SOURce<HwInstance>:LIST:DWELl:LIST {param}')
