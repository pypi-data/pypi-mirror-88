from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Syntax:
	"""Syntax commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("syntax", core, parent)

	def get_all(self) -> str:
		"""SYSTem:HELP:SYNTax:ALL \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:HELP:SYNTax:ALL?')
		return trim_str_response(response)

	def get_value(self) -> str:
		"""SYSTem:HELP:SYNTax \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:HELP:SYNTax?')
		return trim_str_response(response)
