from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Set:
	"""Set commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("set", core, parent)

	def set(self, err_code: int, path: int) -> None:
		"""TEST:SERRor:SET \n
		No command help available \n
			:param err_code: No help available
			:param path: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('err_code', err_code, DataType.Integer), ArgSingle('path', path, DataType.Integer))
		self._core.io.write(f'TEST:SERRor:SET {param}'.rstrip())
