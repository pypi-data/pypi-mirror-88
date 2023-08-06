from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Serial:
	"""Serial commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("serial", core, parent)

	# noinspection PyTypeChecker
	def get_baud(self) -> enums.Rs232BdRate:
		"""SYSTem:COMMunicate:SERial:BAUD \n
		Defines the baudrate for the serial remote control interface. \n
			:return: baud: 2400| 4800| 9600| 19200| 38400| 57600| 115200
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SERial:BAUD?')
		return Conversions.str_to_scalar_enum(response, enums.Rs232BdRate)

	def set_baud(self, baud: enums.Rs232BdRate) -> None:
		"""SYSTem:COMMunicate:SERial:BAUD \n
		Defines the baudrate for the serial remote control interface. \n
			:param baud: 2400| 4800| 9600| 19200| 38400| 57600| 115200
		"""
		param = Conversions.enum_scalar_to_str(baud, enums.Rs232BdRate)
		self._core.io.write(f'SYSTem:COMMunicate:SERial:BAUD {param}')

	# noinspection PyTypeChecker
	def get_parity(self) -> enums.Parity:
		"""SYSTem:COMMunicate:SERial:PARity \n
		Enters the parity for the serial remote control interface. \n
			:return: parity: NONE| ODD| EVEN
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SERial:PARity?')
		return Conversions.str_to_scalar_enum(response, enums.Parity)

	def set_parity(self, parity: enums.Parity) -> None:
		"""SYSTem:COMMunicate:SERial:PARity \n
		Enters the parity for the serial remote control interface. \n
			:param parity: NONE| ODD| EVEN
		"""
		param = Conversions.enum_scalar_to_str(parity, enums.Parity)
		self._core.io.write(f'SYSTem:COMMunicate:SERial:PARity {param}')

	def get_resource(self) -> str:
		"""SYSTem:COMMunicate:SERial:RESource \n
		Queries the visa resource string for the serial remote control interface. This string is used for remote control of the
		instrument. \n
			:return: resource: string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SERial:RESource?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_sbits(self) -> enums.Count:
		"""SYSTem:COMMunicate:SERial:SBITs \n
		Defines the number of stop bits for the serial remote control interface. \n
			:return: sbits: 1| 2
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SERial:SBITs?')
		return Conversions.str_to_scalar_enum(response, enums.Count)

	def set_sbits(self, sbits: enums.Count) -> None:
		"""SYSTem:COMMunicate:SERial:SBITs \n
		Defines the number of stop bits for the serial remote control interface. \n
			:param sbits: 1| 2
		"""
		param = Conversions.enum_scalar_to_str(sbits, enums.Count)
		self._core.io.write(f'SYSTem:COMMunicate:SERial:SBITs {param}')
