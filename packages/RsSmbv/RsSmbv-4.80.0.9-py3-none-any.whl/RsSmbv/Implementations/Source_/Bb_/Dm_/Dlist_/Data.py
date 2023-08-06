from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def set(self, data: List[str]) -> None:
		"""[SOURce<HW>]:BB:DM:DLISt:DATA \n
		The Setting command sends the bit data to the selected data list. Any existing content in the list is overwritten. This
		command only writes data into the data section of the file. Data can be sent as block data in binary or packet format
		(FORMat ASCii | PACKed) , each byte being interpreted as 8 data bits. When binary data transmission is in use, use the
		command SYSTem:COMMunicate:GPIB:LTERminator EOI to set the termination character mode to ‘EOI control data message only’
		so that a random LF in the data sequence is not interpreted as End, thereby prematurely terminating the data transmission.
		The command ...LTER STAN resets the mode. According to the specifications, the byte sequence is defined as 'most
		significant byte first'. The query reads out the data part of the list file. If the query is expanded by using the two
		parameters <Start> and <Count>, the list is read out in smaller sections. Without the parameters the total length is
		always read out starting from address 1. *RST has no effect on data lists. \n
			:param data: integer bit data
		"""
		param = Conversions.list_to_csv_str(data)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:DLISt:DATA {param}')

	def get(self, start: int = None, count: int = None) -> List[str]:
		"""[SOURce<HW>]:BB:DM:DLISt:DATA \n
		The Setting command sends the bit data to the selected data list. Any existing content in the list is overwritten. This
		command only writes data into the data section of the file. Data can be sent as block data in binary or packet format
		(FORMat ASCii | PACKed) , each byte being interpreted as 8 data bits. When binary data transmission is in use, use the
		command SYSTem:COMMunicate:GPIB:LTERminator EOI to set the termination character mode to ‘EOI control data message only’
		so that a random LF in the data sequence is not interpreted as End, thereby prematurely terminating the data transmission.
		The command ...LTER STAN resets the mode. According to the specifications, the byte sequence is defined as 'most
		significant byte first'. The query reads out the data part of the list file. If the query is expanded by using the two
		parameters <Start> and <Count>, the list is read out in smaller sections. Without the parameters the total length is
		always read out starting from address 1. *RST has no effect on data lists. \n
			:param start: integer Range: 1 to 2147483647
			:param count: integer Range: 1 to 2147483647
			:return: data: integer bit data"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('start', start, DataType.Integer, True), ArgSingle('count', count, DataType.Integer, True))
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DM:DLISt:DATA? {param}'.rstrip())
		return Conversions.str_to_str_list(response)

	def set_append(self, bits: List[str]) -> None:
		"""[SOURce<HW>]:BB:DM:DLISt:DATA:APPend \n
		Appends the bit data onto the end of the existing data in the selected data list. Existing content in the data list is
		not overwritten. Hence, you can create long data lists piecemeal. The command cannot be used with an empty data list,
		like for example data lists that has just been created. Use the command method RsSmbv.Source.Bb.Dm.Dlist.Data.set first
		and enter modulation data in the list. *RST has no effect on data lists. \n
			:param bits: 0 | 1 {,0 | 1 } | block data
		"""
		param = Conversions.list_to_csv_str(bits)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:DLISt:DATA:APPend {param}')
