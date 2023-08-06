from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, data_set: int, source_file: str) -> None:
		"""MMEMory:LOAD:STATe \n
		Loads the specified file stored under the specified name in an internal memory. After the file has been loaded, the
		instrument setting must be activated using an *RCL command. \n
			:param data_set: No help available
			:param source_file: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('data_set', data_set, DataType.Integer), ArgSingle('source_file', source_file, DataType.String))
		self._core.io.write(f'MMEMory:LOAD:STATe {param}'.rstrip())
