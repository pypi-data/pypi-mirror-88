from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mtch:
	"""Mtch commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mtch", core, parent)

	# noinspection PyTypeChecker
	def get_csap(self) -> enums.EutraMtchSfAllPer:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:MTCH:CSAP \n
		Defines the period during which resources corresponding with field commonSF-Alloc are divided between the (P) MCH that
		are configured for this MBSFN area. \n
			:return: alloc_period: AP4| AP8| AP16| AP32| AP64| AP128| AP256
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:MTCH:CSAP?')
		return Conversions.str_to_scalar_enum(response, enums.EutraMtchSfAllPer)

	def set_csap(self, alloc_period: enums.EutraMtchSfAllPer) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:MTCH:CSAP \n
		Defines the period during which resources corresponding with field commonSF-Alloc are divided between the (P) MCH that
		are configured for this MBSFN area. \n
			:param alloc_period: AP4| AP8| AP16| AP32| AP64| AP128| AP256
		"""
		param = Conversions.enum_scalar_to_str(alloc_period, enums.EutraMtchSfAllPer)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:MTCH:CSAP {param}')

	def get_npmchs(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:MTCH:NPMChs \n
		Defines the number of PMCHs in this MBSFN area. \n
			:return: num_of_pmchs: int Range: 1 to 15
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:MTCH:NPMChs?')
		return Conversions.str_to_int(response)

	def set_npmchs(self, num_of_pmchs: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:MTCH:NPMChs \n
		Defines the number of PMCHs in this MBSFN area. \n
			:param num_of_pmchs: int Range: 1 to 15
		"""
		param = Conversions.decimal_value_to_str(num_of_pmchs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:MTCH:NPMChs {param}')
