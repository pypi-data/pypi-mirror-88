from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Name:
	"""Name commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("name", core, parent)

	def get_detailed(self) -> str:
		"""SYSTem:LOCK:NAME:DETailed \n
		No command help available \n
			:return: details: No help available
		"""
		response = self._core.io.query_str('SYSTem:LOCK:NAME:DETailed?')
		return trim_str_response(response)

	def get_value(self) -> str:
		"""SYSTem:LOCK:NAME \n
		No command help available \n
			:return: name: No help available
		"""
		response = self._core.io.query_str('SYSTem:LOCK:NAME?')
		return trim_str_response(response)
