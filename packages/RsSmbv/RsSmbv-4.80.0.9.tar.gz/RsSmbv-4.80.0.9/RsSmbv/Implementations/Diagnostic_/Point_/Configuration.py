from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Configuration:
	"""Configuration commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("configuration", core, parent)

	def set(self, dev_board: str, point: str, data: str) -> None:
		"""DIAGnostic<HW>:POINt:CONFiguration \n
		No command help available \n
			:param dev_board: No help available
			:param point: No help available
			:param data: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('dev_board', dev_board, DataType.String), ArgSingle('point', point, DataType.String), ArgSingle('data', data, DataType.String))
		self._core.io.write(f'DIAGnostic<HwInstance>:POINt:CONFiguration {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Dev_Board: str: No parameter help available
			- Point: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Dev_Board'),
			ArgStruct.scalar_str('Point')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dev_Board: str = None
			self.Point: str = None

	def get(self) -> GetStruct:
		"""DIAGnostic<HW>:POINt:CONFiguration \n
		No command help available \n
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		return self._core.io.query_struct(f'DIAGnostic<HwInstance>:POINt:CONFiguration?', self.__class__.GetStruct())
