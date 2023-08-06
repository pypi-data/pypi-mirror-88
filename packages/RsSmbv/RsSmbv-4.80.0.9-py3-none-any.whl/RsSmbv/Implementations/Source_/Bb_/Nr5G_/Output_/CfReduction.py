from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CfReduction:
	"""CfReduction commands group definition. 6 total commands, 0 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cfReduction", core, parent)

	# noinspection PyTypeChecker
	def get_algorithm(self) -> enums.CrestFactoralgorithm:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:ALGorithm \n
		No command help available \n
			:return: cfr_algorithm: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:ALGorithm?')
		return Conversions.str_to_scalar_enum(response, enums.CrestFactoralgorithm)

	def set_algorithm(self, cfr_algorithm: enums.CrestFactoralgorithm) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:ALGorithm \n
		No command help available \n
			:param cfr_algorithm: No help available
		"""
		param = Conversions.enum_scalar_to_str(cfr_algorithm, enums.CrestFactoralgorithm)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:ALGorithm {param}')

	def get_iterations(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:ITERations \n
		No command help available \n
			:return: max_iteration: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:ITERations?')
		return Conversions.str_to_int(response)

	def set_iterations(self, max_iteration: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:ITERations \n
		No command help available \n
			:param max_iteration: No help available
		"""
		param = Conversions.decimal_value_to_str(max_iteration)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:ITERations {param}')

	def get_oc_factor(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:OCFactor \n
		No command help available \n
			:return: original_cfr: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:OCFactor?')
		return Conversions.str_to_int(response)

	def get_rc_factor(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:RCFactor \n
		No command help available \n
			:return: resulting_cfr: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:RCFactor?')
		return Conversions.str_to_int(response)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:STATe \n
		No command help available \n
			:return: crest_factor_stat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, crest_factor_stat: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:STATe \n
		No command help available \n
			:param crest_factor_stat: No help available
		"""
		param = Conversions.bool_to_str(crest_factor_stat)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:STATe {param}')

	def get_tcr_factor(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:TCRFactor \n
		No command help available \n
			:return: target_crf: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:TCRFactor?')
		return Conversions.str_to_float(response)

	def set_tcr_factor(self, target_crf: float) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:CFReduction:TCRFactor \n
		No command help available \n
			:param target_crf: No help available
		"""
		param = Conversions.decimal_value_to_str(target_crf)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:CFReduction:TCRFactor {param}')
