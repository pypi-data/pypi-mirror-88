from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Length:
	"""Length commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("length", core, parent)

	def get(self, path: str = None) -> int:
		"""MMEMory:DCATalog:LENGth \n
		Returns the number of subdirectories in the current or specified directory. \n
			:param path: String parameter to specify the directory. If the directory is omitted, the command queries the contents of the current directory, to be queried with method RsSmbv.MassMemory.currentDirectory command.
			:return: directory_count: integer Number of parent and subdirectories."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('path', path, DataType.String, True))
		response = self._core.io.query_str(f'MMEMory:DCATalog:LENGth? {param}'.rstrip())
		return Conversions.str_to_int(response)
