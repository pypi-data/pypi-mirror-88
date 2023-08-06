from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trial:
	"""Trial commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trial", core, parent)

	def get_list_py(self) -> List[str]:
		"""SYSTem:OPTion:TRIal:LIST \n
		No command help available \n
			:return: trial_opt_list: No help available
		"""
		response = self._core.io.query_str('SYSTem:OPTion:TRIal:LIST?')
		return Conversions.str_to_str_list(response)

	def get_state(self) -> bool:
		"""SYSTem:OPTion:TRIal:[STATe] \n
		No command help available \n
			:return: trial_opt_state: No help available
		"""
		response = self._core.io.query_str('SYSTem:OPTion:TRIal:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, trial_opt_state: bool) -> None:
		"""SYSTem:OPTion:TRIal:[STATe] \n
		No command help available \n
			:param trial_opt_state: No help available
		"""
		param = Conversions.bool_to_str(trial_opt_state)
		self._core.io.write(f'SYSTem:OPTion:TRIal:STATe {param}')
