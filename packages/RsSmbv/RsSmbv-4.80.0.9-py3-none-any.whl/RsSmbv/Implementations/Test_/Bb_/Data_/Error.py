from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Error:
	"""Error commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("error", core, parent)

	def get_rate(self) -> float:
		"""TEST:BB:DATA:ERRor:RATE \n
		No command help available \n
			:return: error_rate: No help available
		"""
		response = self._core.io.query_str('TEST:BB:DATA:ERRor:RATE?')
		return Conversions.str_to_float(response)

	def set_rate(self, error_rate: float) -> None:
		"""TEST:BB:DATA:ERRor:RATE \n
		No command help available \n
			:param error_rate: No help available
		"""
		param = Conversions.decimal_value_to_str(error_rate)
		self._core.io.write(f'TEST:BB:DATA:ERRor:RATE {param}')
