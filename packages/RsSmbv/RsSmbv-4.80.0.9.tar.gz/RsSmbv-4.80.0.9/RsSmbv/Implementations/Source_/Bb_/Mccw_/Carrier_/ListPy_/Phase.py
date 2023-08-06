from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Phase:
	"""Phase commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("phase", core, parent)

	def set(self, phases: List[float]) -> None:
		"""[SOURce<HW>]:BB:MCCW:CARRier:LIST:PHASe \n
		Sets the start phase of the carrier with the aid of a value list. \n
			:param phases: No help available
		"""
		param = Conversions.list_to_csv_str(phases)
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:CARRier:LIST:PHASe {param}')

	def get(self, start: int = None, count: int = None) -> List[float]:
		"""[SOURce<HW>]:BB:MCCW:CARRier:LIST:PHASe \n
		Sets the start phase of the carrier with the aid of a value list. \n
			:param start: integer start carrier index Range: 0 to lastCarrier
			:param count: integer number of carriers in the carrier range, starting from the Start carrier Range: 1 to max
			:return: phases: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Integer, True), ArgSingle('count', count, DataType.Integer, True))
		response = self._core.io.query_bin_or_ascii_float_list(f'SOURce<HwInstance>:BB:MCCW:CARRier:LIST:PHASe? {param}'.rstrip())
		return response
