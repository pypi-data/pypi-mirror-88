from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class K145:
	"""K145 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("k145", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:K145:STATe \n
		No command help available \n
			:return: opt_state_k_145: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:K145:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, opt_state_k_145: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:K145:STATe \n
		No command help available \n
			:param opt_state_k_145: No help available
		"""
		param = Conversions.bool_to_str(opt_state_k_145)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:K145:STATe {param}')
