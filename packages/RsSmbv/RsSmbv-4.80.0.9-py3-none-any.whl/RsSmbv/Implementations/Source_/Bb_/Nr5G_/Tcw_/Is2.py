from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Is2:
	"""Is2 commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("is2", core, parent)

	# noinspection PyTypeChecker
	def get_if_type(self) -> enums.InterfererTypeCw:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS2:IFTYpe \n
		No command help available \n
			:return: interferer_type_2: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS2:IFTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.InterfererTypeCw)

	def get_plevel(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS2:PLEVel \n
		Queries the power level of the interfering signal. \n
			:return: is_2_powel_level: float Range: -145 to 20, Unit: dBm
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS2:PLEVel?')
		return Conversions.str_to_float(response)

	def get_rf_frequency(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:TCW:IS2:RFFRequency \n
		Queries the center frequency of the interfering signal 1 and 2. \n
			:return: is_2_rf_frequency: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:IS2:RFFRequency?')
		return Conversions.str_to_int(response)
