from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	# noinspection PyTypeChecker
	def get_amode(self) -> enums.PowerAttMode:
		"""[SOURce<HW>]:LIST:POWer:AMODe \n
		No command help available \n
			:return: am_ode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:POWer:AMODe?')
		return Conversions.str_to_scalar_enum(response, enums.PowerAttMode)

	def set_amode(self, am_ode: enums.PowerAttMode) -> None:
		"""[SOURce<HW>]:LIST:POWer:AMODe \n
		No command help available \n
			:param am_ode: No help available
		"""
		param = Conversions.enum_scalar_to_str(am_ode, enums.PowerAttMode)
		self._core.io.write(f'SOURce<HwInstance>:LIST:POWer:AMODe {param}')

	def get_points(self) -> int:
		"""[SOURce<HW>]:LIST:POWer:POINts \n
		Queries the number (points) of level entries in the selected list. \n
			:return: points: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:POWer:POINts?')
		return Conversions.str_to_int(response)

	def get_value(self) -> List[float]:
		"""[SOURce<HW>]:LIST:POWer \n
		Enters the level values in the selected list. The number of level values must correspond to the number of frequency
		values. Existing data is overwritten. \n
			:return: power: Power#1{, Power#2, ...} | block data You can either enter the data as a list of numbers, or as binary block data. The list of numbers can be of any length, with the list entries separated by commas. In binary block format, 8 (4) bytes are always interpreted as a floating-point number with double accuracy. See also :​FORMat[:​DATA]. Range: depends on the installed options , Unit: dBm
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce<HwInstance>:LIST:POWer?')
		return response

	def set_value(self, power: List[float]) -> None:
		"""[SOURce<HW>]:LIST:POWer \n
		Enters the level values in the selected list. The number of level values must correspond to the number of frequency
		values. Existing data is overwritten. \n
			:param power: Power#1{, Power#2, ...} | block data You can either enter the data as a list of numbers, or as binary block data. The list of numbers can be of any length, with the list entries separated by commas. In binary block format, 8 (4) bytes are always interpreted as a floating-point number with double accuracy. See also :​FORMat[:​DATA]. Range: depends on the installed options , Unit: dBm
		"""
		param = Conversions.list_to_csv_str(power)
		self._core.io.write(f'SOURce<HwInstance>:LIST:POWer {param}')
