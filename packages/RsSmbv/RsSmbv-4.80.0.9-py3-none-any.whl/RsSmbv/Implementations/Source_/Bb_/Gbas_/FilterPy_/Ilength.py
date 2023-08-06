from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ilength:
	"""Ilength commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ilength", core, parent)

	def get_auto(self) -> bool:
		"""[SOURce<HW>]:BB:GBAS:FILTer:ILENgth:AUTO \n
		No command help available \n
			:return: auto: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GBAS:FILTer:ILENgth:AUTO?')
		return Conversions.str_to_bool(response)

	def set_auto(self, auto: bool) -> None:
		"""[SOURce<HW>]:BB:GBAS:FILTer:ILENgth:AUTO \n
		No command help available \n
			:param auto: No help available
		"""
		param = Conversions.bool_to_str(auto)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:FILTer:ILENgth:AUTO {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:BB:GBAS:FILTer:ILENgth \n
		No command help available \n
			:return: ilrngth: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GBAS:FILTer:ILENgth?')
		return Conversions.str_to_float(response)

	def set_value(self, ilrngth: float) -> None:
		"""[SOURce<HW>]:BB:GBAS:FILTer:ILENgth \n
		No command help available \n
			:param ilrngth: No help available
		"""
		param = Conversions.decimal_value_to_str(ilrngth)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:FILTer:ILENgth {param}')
