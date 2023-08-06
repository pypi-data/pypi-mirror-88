from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Shared:
	"""Shared commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("shared", core, parent)

	def get(self, name: str, timeout_ms: int) -> int:
		"""SYSTem:LOCK:REQuest:SHARed \n
		No command help available \n
			:param name: No help available
			:param timeout_ms: No help available
			:return: success: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('name', name, DataType.String), ArgSingle('timeout_ms', timeout_ms, DataType.Integer))
		response = self._core.io.query_str(f'SYSTem:LOCK:REQuest:SHARed? {param}'.rstrip())
		return Conversions.str_to_int(response)
