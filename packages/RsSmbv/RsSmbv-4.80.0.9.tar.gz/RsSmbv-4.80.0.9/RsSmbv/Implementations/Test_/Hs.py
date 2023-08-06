from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hs:
	"""Hs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hs", core, parent)

	def set(self, interface: str, set_py: str) -> None:
		"""TEST:HS \n
		No command help available \n
			:param interface: No help available
			:param set_py: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('interface', interface, DataType.String), ArgSingle('set_py', set_py, DataType.String))
		self._core.io.write(f'TEST:HS {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Interface: str: No parameter help available
			- Result: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Interface'),
			ArgStruct.scalar_str('Result')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Interface: str = None
			self.Result: str = None

	def get(self, get_py: str) -> GetStruct:
		"""TEST:HS \n
		No command help available \n
			:param get_py: No help available
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		param = Conversions.value_to_quoted_str(get_py)
		return self._core.io.query_struct(f'TEST:HS? {param}', self.__class__.GetStruct())
