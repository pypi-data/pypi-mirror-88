from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ethernet:
	"""Ethernet commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ethernet", core, parent)

	def get_active(self) -> str:
		"""SYSTem:COMMunicate:SCPI:ETHernet:[ACTive] \n
		No command help available \n
			:return: active_connectio: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SCPI:ETHernet:ACTive?')
		return trim_str_response(response)
