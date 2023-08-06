from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Synchronize:
	"""Synchronize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("synchronize", core, parent)

	def get(self, time: str) -> str:
		"""SYSTem:SRTime:SYNChronize \n
		No command help available \n
			:param time: No help available
			:return: time: No help available"""
		param = Conversions.value_to_quoted_str(time)
		response = self._core.io.query_str(f'SYSTem:SRTime:SYNChronize? {param}')
		return trim_str_response(response)
