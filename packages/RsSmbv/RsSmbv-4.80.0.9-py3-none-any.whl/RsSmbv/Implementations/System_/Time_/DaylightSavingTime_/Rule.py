from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rule:
	"""Rule commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rule", core, parent)

	def get_catalog(self) -> str:
		"""SYSTem:TIME:DSTime:RULE:CATalog \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:TIME:DSTime:RULE:CATalog?')
		return trim_str_response(response)

	def get_value(self) -> str:
		"""SYSTem:TIME:DSTime:RULE \n
		No command help available \n
			:return: pseudo_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:TIME:DSTime:RULE?')
		return trim_str_response(response)

	def set_value(self, pseudo_string: str) -> None:
		"""SYSTem:TIME:DSTime:RULE \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:TIME:DSTime:RULE {param}')
