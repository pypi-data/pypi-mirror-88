from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def get_variable(self) -> float:
		"""[SOURce]:ROSCillator:EXTernal:FREQuency:VARiable \n
		Specifies the user-defined external reference frequency. \n
			:return: frequency: float Range: 1E6 to 100E6, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:EXTernal:FREQuency:VARiable?')
		return Conversions.str_to_float(response)

	def set_variable(self, frequency: float) -> None:
		"""[SOURce]:ROSCillator:EXTernal:FREQuency:VARiable \n
		Specifies the user-defined external reference frequency. \n
			:param frequency: float Range: 1E6 to 100E6, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce:ROSCillator:EXTernal:FREQuency:VARiable {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.RoscFreqExt:
		"""[SOURce]:ROSCillator:EXTernal:FREQuency \n
		Sets the frequency of the external reference. \n
			:return: frequency: 100MHZ| 1GHZ| VARiable| 10MHZ
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:EXTernal:FREQuency?')
		return Conversions.str_to_scalar_enum(response, enums.RoscFreqExt)

	def set_value(self, frequency: enums.RoscFreqExt) -> None:
		"""[SOURce]:ROSCillator:EXTernal:FREQuency \n
		Sets the frequency of the external reference. \n
			:param frequency: 100MHZ| 1GHZ| VARiable| 10MHZ
		"""
		param = Conversions.enum_scalar_to_str(frequency, enums.RoscFreqExt)
		self._core.io.write(f'SOURce:ROSCillator:EXTernal:FREQuency {param}')
