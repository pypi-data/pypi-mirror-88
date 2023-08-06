from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Impairments:
	"""Impairments commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("impairments", core, parent)

	def get_foffset(self) -> int:
		"""[SOURce<HW>]:BB:HUWB:IMPairments:FOFFset \n
		Sets the symbol timing error of the impaiment symbols. \n
			:return: fo_ffset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:IMPairments:FOFFset?')
		return Conversions.str_to_int(response)

	def set_foffset(self, fo_ffset: int) -> None:
		"""[SOURce<HW>]:BB:HUWB:IMPairments:FOFFset \n
		Sets the symbol timing error of the impaiment symbols. \n
			:param fo_ffset: integer Range: -300 to 300
		"""
		param = Conversions.decimal_value_to_str(fo_ffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:IMPairments:FOFFset {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:HUWB:IMPairments:STATe \n
		Sets the symbol timing error of the impaiment symbols. \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:IMPairments:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:HUWB:IMPairments:STATe \n
		Sets the symbol timing error of the impaiment symbols. \n
			:param state: integer Range: -300 to 300
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:IMPairments:STATe {param}')

	def get_st_error(self) -> int:
		"""[SOURce<HW>]:BB:HUWB:IMPairments:STERror \n
		Sets the symbol timing error of the impaiment symbols. \n
			:return: st_error: integer Range: -300 to 300
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:IMPairments:STERror?')
		return Conversions.str_to_int(response)

	def set_st_error(self, st_error: int) -> None:
		"""[SOURce<HW>]:BB:HUWB:IMPairments:STERror \n
		Sets the symbol timing error of the impaiment symbols. \n
			:param st_error: integer Range: -300 to 300
		"""
		param = Conversions.decimal_value_to_str(st_error)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:IMPairments:STERror {param}')
