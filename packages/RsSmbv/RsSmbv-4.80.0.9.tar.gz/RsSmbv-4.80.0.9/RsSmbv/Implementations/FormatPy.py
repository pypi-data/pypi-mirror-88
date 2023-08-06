from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FormatPy:
	"""FormatPy commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("formatPy", core, parent)

	# noinspection PyTypeChecker
	def get_border(self) -> enums.ByteOrder:
		"""FORMat:BORDer \n
		Determines the sequence of bytes within a binary block. This only affects blocks which use the IEEE754 format internally. \n
			:return: border: NORMal| SWAPped NORMal Expects/sends the least significant byte of each IEEE754 floating-point number first and the most significant byte last. SWAPped Expects/sends the most significant byte of each IEEE754 floating-point number first and the least significant byte last.
		"""
		response = self._core.io.query_str('FORMat:BORDer?')
		return Conversions.str_to_scalar_enum(response, enums.ByteOrder)

	def set_border(self, border: enums.ByteOrder) -> None:
		"""FORMat:BORDer \n
		Determines the sequence of bytes within a binary block. This only affects blocks which use the IEEE754 format internally. \n
			:param border: NORMal| SWAPped NORMal Expects/sends the least significant byte of each IEEE754 floating-point number first and the most significant byte last. SWAPped Expects/sends the most significant byte of each IEEE754 floating-point number first and the least significant byte last.
		"""
		param = Conversions.enum_scalar_to_str(border, enums.ByteOrder)
		self._core.io.write(f'FORMat:BORDer {param}')

	# noinspection PyTypeChecker
	def get_sregister(self) -> enums.FormStatReg:
		"""FORMat:SREGister \n
		Determines the numeric format for responses of the status register. \n
			:return: format_py: ASCii| BINary| HEXadecimal| OCTal ASCii Returns the register content as a decimal number. BINary|HEXadecimal|OCTal Returns the register content either as a binary, hexadecimal or octal number. According to the selected format, the number starts with #B (binary) , #H (hexadecimal) or #O (octal) .
		"""
		response = self._core.io.query_str('FORMat:SREGister?')
		return Conversions.str_to_scalar_enum(response, enums.FormStatReg)

	def set_sregister(self, format_py: enums.FormStatReg) -> None:
		"""FORMat:SREGister \n
		Determines the numeric format for responses of the status register. \n
			:param format_py: ASCii| BINary| HEXadecimal| OCTal ASCii Returns the register content as a decimal number. BINary|HEXadecimal|OCTal Returns the register content either as a binary, hexadecimal or octal number. According to the selected format, the number starts with #B (binary) , #H (hexadecimal) or #O (octal) .
		"""
		param = Conversions.enum_scalar_to_str(format_py, enums.FormStatReg)
		self._core.io.write(f'FORMat:SREGister {param}')

	# noinspection PyTypeChecker
	def get_data(self) -> enums.FormData:
		"""FORMat:[DATA] \n
		Determines the data format the instrument uses to return data via the IEC/IEEE bus. The instrument automatically detects
		the data format used by the controller, and assigns it accordingly. Data format determined by this SCPI command is in
		this case irrelevant. \n
			:return: data: ASCii| PACKed ASCii Transfers numerical data as plain text separated by commas. PACKed Transfers numerical data as binary block data. The format within the binary data depends on the command. The various binary data formats are explained in the description of the parameter types.
		"""
		response = self._core.io.query_str('FORMat:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.FormData)

	def set_data(self, data: enums.FormData) -> None:
		"""FORMat:[DATA] \n
		Determines the data format the instrument uses to return data via the IEC/IEEE bus. The instrument automatically detects
		the data format used by the controller, and assigns it accordingly. Data format determined by this SCPI command is in
		this case irrelevant. \n
			:param data: ASCii| PACKed ASCii Transfers numerical data as plain text separated by commas. PACKed Transfers numerical data as binary block data. The format within the binary data depends on the command. The various binary data formats are explained in the description of the parameter types.
		"""
		param = Conversions.enum_scalar_to_str(data, enums.FormData)
		self._core.io.write(f'FORMat:DATA {param}')
