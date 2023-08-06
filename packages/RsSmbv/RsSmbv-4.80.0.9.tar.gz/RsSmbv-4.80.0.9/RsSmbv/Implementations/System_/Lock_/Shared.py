from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Shared:
	"""Shared commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("shared", core, parent)

	def get_string(self) -> str:
		"""SYSTem:LOCK:SHARed:STRing \n
		No command help available \n
			:return: string: No help available
		"""
		response = self._core.io.query_str('SYSTem:LOCK:SHARed:STRing?')
		return trim_str_response(response)
