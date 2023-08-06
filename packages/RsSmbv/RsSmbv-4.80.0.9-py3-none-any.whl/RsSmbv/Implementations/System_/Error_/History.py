from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class History:
	"""History commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("history", core, parent)

	def clear(self) -> None:
		"""SYSTem:ERRor:HISTory:CLEar \n
		Clears the error history. \n
		"""
		self._core.io.write(f'SYSTem:ERRor:HISTory:CLEar')

	def clear_with_opc(self) -> None:
		"""SYSTem:ERRor:HISTory:CLEar \n
		Clears the error history. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:ERRor:HISTory:CLEar')

	def get_value(self) -> str:
		"""SYSTem:ERRor:HISTory \n
		No command help available \n
			:return: error_history: No help available
		"""
		response = self._core.io.query_str('SYSTem:ERRor:HISTory?')
		return trim_str_response(response)
