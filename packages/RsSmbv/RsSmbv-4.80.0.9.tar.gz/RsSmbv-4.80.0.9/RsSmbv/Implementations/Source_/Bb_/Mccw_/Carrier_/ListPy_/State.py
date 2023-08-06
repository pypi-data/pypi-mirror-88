from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, states: List[int]) -> None:
		"""[SOURce<HW>]:BB:MCCW:CARRier:LIST:STATe \n
		Switches the carrier on or off with the aid of a value list. The first value in the list is assigned to the carrier with
		index 0, the second value to the carrier with index 1, etc. The maximum length corresponds to the maximum number of multi
		carriers. There is no need to enter all the values every time. Values not set by the value list are set with the default
		values provided they have already been explicitly set by a previous command. If this is the case, the values continue to
		apply until overwritten. \n
			:param states: No help available
		"""
		param = Conversions.list_to_csv_str(states)
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:CARRier:LIST:STATe {param}')

	def get(self, start: int, count: int) -> List[int]:
		"""[SOURce<HW>]:BB:MCCW:CARRier:LIST:STATe \n
		Switches the carrier on or off with the aid of a value list. The first value in the list is assigned to the carrier with
		index 0, the second value to the carrier with index 1, etc. The maximum length corresponds to the maximum number of multi
		carriers. There is no need to enter all the values every time. Values not set by the value list are set with the default
		values provided they have already been explicitly set by a previous command. If this is the case, the values continue to
		apply until overwritten. \n
			:param start: integer start carrier index Range: 0 to lastCarrier
			:param count: integer number of carriers in the carrier range, starting from the Start carrier Range: 1 to lastCarrier
			:return: states: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Integer), ArgSingle('count', count, DataType.Integer))
		response = self._core.io.query_bin_or_ascii_int_list(f'SOURce<HwInstance>:BB:MCCW:CARRier:LIST:STATe? {param}'.rstrip())
		return response
