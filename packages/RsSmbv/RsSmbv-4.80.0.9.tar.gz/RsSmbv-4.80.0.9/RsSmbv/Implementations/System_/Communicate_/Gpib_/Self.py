from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Self:
	"""Self commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("self", core, parent)

	def get_address(self) -> int:
		"""SYSTem:COMMunicate:GPIB:[SELF]:ADDRess \n
		Sets the GPIB address. \n
			:return: address: integer Range: 0 to 30
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:GPIB:SELF:ADDRess?')
		return Conversions.str_to_int(response)

	def set_address(self, address: int) -> None:
		"""SYSTem:COMMunicate:GPIB:[SELF]:ADDRess \n
		Sets the GPIB address. \n
			:param address: integer Range: 0 to 30
		"""
		param = Conversions.decimal_value_to_str(address)
		self._core.io.write(f'SYSTem:COMMunicate:GPIB:SELF:ADDRess {param}')
