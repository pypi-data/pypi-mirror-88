from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.Utilities import trim_str_response
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BgInfo:
	"""BgInfo commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bgInfo", core, parent)

	def get(self, board: str = None) -> str:
		"""DIAGnostic<HW>:BGINfo \n
		Queries information on the modules available in the instrument, using the variant and revision state. \n
			:param board: string Module name, as queried with the command method RsSmbv.Diagnostic.BgInfo.catalog. To retrieve a complete list of all modules, omit the parameter. The length of the list is variable and depends on the instrument equipment configuration.
			:return: bg_info: Module name Module stock number incl. variant Module revision Module serial number List of comma-separated entries, one entry per module. Each entry for one module consists of four parts that are separated by space characters."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('board', board, DataType.String, True))
		response = self._core.io.query_str(f'DIAGnostic<HwInstance>:BGINfo? {param}'.rstrip())
		return trim_str_response(response)

	def get_catalog(self) -> List[str]:
		"""DIAGnostic<HW>:BGINfo:CATalog \n
		Queries the names of the assemblies available in the instrument. \n
			:return: catalog: string List of all assemblies; the values are separated by commas The length of the list is variable and depends on the instrument equipment configuration.
		"""
		response = self._core.io.query_str('DIAGnostic<HwInstance>:BGINfo:CATalog?')
		return Conversions.str_to_str_list(response)
