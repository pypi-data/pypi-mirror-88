from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Clist:
	"""Clist commands group definition. 8 total commands, 0 Sub-groups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("clist", core, parent)

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:DM:CLISt:CATalog \n
		Reads out the list files present in the default directory (see method RsSmbv.MassMemory.currentDirectory) .
			Table Header: List type / Command / File extension \n
			- Data list / ...:DLISt... / *.dm_iqd
			- Control list / ...:CLISt... / *.dm_iqc
			- User filter files / ...:FLISt... / *.vaf
			- User mapping lists / ...:MLISt... / *.vam
		Refer to 'Accessing Files in the Default or in a Specified Directory' for general information on file handling in the
		default and a specific directory. \n
			:return: catalog: 'filename1,filename2,...' Returns a string of file names separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:CLISt:CATalog?')
		return Conversions.str_to_str_list(response)

	def copy(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DM:CLISt:COPY \n
		Copies the selected data list (*.dm_iqd) / control list (*.dm_iqc) as a new list with name specified by <Filename>. If a
		list with the specified name exists, it is overwritten. If it does not yet exist, it is created. The source file has to
		be available in the default directory (see method RsSmbv.MassMemory.currentDirectory) . Refer to 'Accessing Files in the
		Default or in a Specified Directory' for general information on file handling in the default and a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:CLISt:COPY {param}')

	def set_data(self, data: List[int]) -> None:
		"""[SOURce<HW>]:BB:DM:CLISt:DATA \n
		Sends the data to the currently selected control list. If the list already contains data, it is overwritten. This command
		only writes data into the data section of the file. The values for the control signals are sent, arranged in an 8-bit
		value as defined in Table 'Contents of a control lists'. Contents of a control lists
			Table Header: Signal / Order / Decimal value of bits \n
			- Marker 1 Marker 2 Marker 3 / LSB / 1 2 4
			- Burst / LSB / 16
			- LevAtt1 / LSB / 32
			- CWMod / LSB / 64
			- Hop / MSB / 128
		The data can also be sent as a binary block, each binary block being a 2-byte value in which the 16 bits represent the
		binary values (16-bit unsigned integer, 2 bytes, LSB first) . When binary data transmission is in use, use the command
		SYSTem:COMMunicate:GPIB:LTERminator EOI to set the termination character mode to ‘EOI control data message only’ so that
		a random LF in the data sequence is not interpreted as End, thereby prematurely terminating the data transmission.
		The command ...LTER STAN resets the mode. According to the specifications, the byte sequence is defined as 'most
		significant byte first'. Tip: Control lists are created in binary format. You may however need the control list in an
		ASCII format, e.g for creating a waveform file with R&S WinIQSIM2. Refer to the examples in 'How to Create a Control List
		Using Tag File Format' for description on how to create a control list file in ASCII format manually. *RST has no effect
		on data lists. \n
			:param data: string
		"""
		param = Conversions.list_to_csv_str(data)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:CLISt:DATA {param}')

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DM:CLISt:DELete \n
		Deletes the specified list from the default directory (see method RsSmbv.MassMemory.currentDirectory) or from the
		directory specified with the absolute file path. Refer to 'Accessing Files in the Default or in a Specified Directory'
		for general information on file handling in the default and a specific directory.
			Table Header: List type / Command / File extension \n
			- Data list / ...:DLISt... / *.dm_iqd
			- Control list / ...:CLISt... / *.dm_iqc
			- User standard / ...:ULISt... / *.dm_stu
			- User filter files / ...:FLISt... / *.vaf
			- User mapping lists / ...:MLISt... / *.vam \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:CLISt:DELete {param}')

	def get_free(self) -> int:
		"""[SOURce<HW>]:BB:DM:CLISt:FREE \n
		Queries the list free memory.
			Table Header: List type / Command / File extension \n
			- Data list / ...:DLISt... / *.dm_iqd
			- Control list / ...:CLISt... / *.dm_iqc
			- User filter files / ...:FLISt... / *.vaf
			- User mapping lists / ...:MLISt... / *.vam \n
			:return: free: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:CLISt:FREE?')
		return Conversions.str_to_int(response)

	def get_points(self) -> int:
		"""[SOURce<HW>]:BB:DM:CLISt:POINts \n
		Queries the number of lines (2 bytes) in the currently selected list. \n
			:return: points: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:CLISt:POINts?')
		return Conversions.str_to_int(response)

	def get_select(self) -> str:
		"""[SOURce<HW>]:BB:DM:CLISt:SELect \n
		Selects the specified list file from the default directory (see method RsSmbv.MassMemory.currentDirectory) or in the
		directory specified with the absolute file path. If a list with the specified name does not yet exist, it is created. The
		file extension can be omitted. Refer to 'Accessing Files in the Default or in a Specified Directory' for general
		information on file handling in the default and a specific directory.
			Table Header: List type / Command / File extension \n
			- Data list / ...:DLISt... / *.dm_iqd
			- Control list / ...:CLISt... / *.dm_iqc
			- User standard / ...:ULISt... / *.dm_stu
			- User filter files / ...:FLISt... / *.vaf
			- User mapping lists / ...:MLISt... / *.vam \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:CLISt:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:DM:CLISt:SELect \n
		Selects the specified list file from the default directory (see method RsSmbv.MassMemory.currentDirectory) or in the
		directory specified with the absolute file path. If a list with the specified name does not yet exist, it is created. The
		file extension can be omitted. Refer to 'Accessing Files in the Default or in a Specified Directory' for general
		information on file handling in the default and a specific directory.
			Table Header: List type / Command / File extension \n
			- Data list / ...:DLISt... / *.dm_iqd
			- Control list / ...:CLISt... / *.dm_iqc
			- User standard / ...:ULISt... / *.dm_stu
			- User filter files / ...:FLISt... / *.vaf
			- User mapping lists / ...:MLISt... / *.vam \n
			:param filename: list name
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:CLISt:SELect {param}')

	def get_tag(self) -> str:
		"""[SOURce<HW>]:BB:DM:CLISt:TAG \n
		Queries the content of the specified tag in the selected file. \n
			:return: tag: control list,tag name Refer to 'Tags for Waveforms, Data and Control Lists' for description of the available tag formats.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:CLISt:TAG?')
		return trim_str_response(response)
