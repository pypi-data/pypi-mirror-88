from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fa:
	"""Fa commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fa", core, parent)

	# noinspection PyTypeChecker
	def get_fr_allocation(self) -> enums.EutraTcwfReqAlloc:
		"""[SOURce<HW>]:BB:EUTRa:TCW:FA:FRALlocation \n
		Determines the frequency position of the wanted and interfering signal. \n
			:return: frequency_alloc: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:FA:FRALlocation?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwfReqAlloc)

	def set_fr_allocation(self, frequency_alloc: enums.EutraTcwfReqAlloc) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:FA:FRALlocation \n
		Determines the frequency position of the wanted and interfering signal. \n
			:param frequency_alloc: HIGHer| LOWer
		"""
		param = Conversions.enum_scalar_to_str(frequency_alloc, enums.EutraTcwfReqAlloc)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:FA:FRALlocation {param}')

	# noinspection PyTypeChecker
	def get_rb_allocation(self) -> enums.EutraTcwfReqAlloc:
		"""[SOURce<HW>]:BB:EUTRa:TCW:FA:RBALlocation \n
		Determines the frequency position of the wanted and interfering signal. \n
			:return: res_block_alloc: HIGHer| LOWer
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:FA:RBALlocation?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwfReqAlloc)

	def set_rb_allocation(self, res_block_alloc: enums.EutraTcwfReqAlloc) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:FA:RBALlocation \n
		Determines the frequency position of the wanted and interfering signal. \n
			:param res_block_alloc: HIGHer| LOWer
		"""
		param = Conversions.enum_scalar_to_str(res_block_alloc, enums.EutraTcwfReqAlloc)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:FA:RBALlocation {param}')
