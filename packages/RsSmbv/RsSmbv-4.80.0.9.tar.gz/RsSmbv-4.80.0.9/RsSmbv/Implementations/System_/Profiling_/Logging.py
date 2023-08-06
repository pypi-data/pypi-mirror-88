from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Logging:
	"""Logging commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("logging", core, parent)

	def get_state(self) -> bool:
		"""SYSTem:PROFiling:LOGGing:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SYSTem:PROFiling:LOGGing:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SYSTem:PROFiling:LOGGing:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SYSTem:PROFiling:LOGGing:STATe {param}')
