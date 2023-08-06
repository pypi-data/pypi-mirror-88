from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Info:
	"""Info commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("info", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:POWer:INFO:STATe \n
		No command help available \n
			:return: power_info_valid: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:POWer:INFO:STATe?')
		return Conversions.str_to_bool(response)
