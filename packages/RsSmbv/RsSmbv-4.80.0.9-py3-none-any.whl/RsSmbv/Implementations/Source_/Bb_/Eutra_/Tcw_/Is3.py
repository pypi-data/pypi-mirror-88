from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Is3:
	"""Is3 commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("is3", core, parent)

	def get_ort_cover(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS3:ORTCover \n
		No command help available \n
			:return: ortho_cover: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS3:ORTCover?')
		return Conversions.str_to_int(response)

	def get_plevel(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS3:PLEVel \n
		Queries the power level of the interfering signal. \n
			:return: power_level: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS3:PLEVel?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_pr_condition(self) -> enums.EutraTcwPropagCond:
		"""[SOURce<HW>]:BB:EUTRa:TCW:IS3:PRCOndition \n
		No command help available \n
			:return: propag_condition: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:IS3:PRCOndition?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwPropagCond)
