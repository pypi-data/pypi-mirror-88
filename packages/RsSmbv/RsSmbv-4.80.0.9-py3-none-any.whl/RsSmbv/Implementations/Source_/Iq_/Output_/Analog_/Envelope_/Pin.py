from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pin:
	"""Pin commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pin", core, parent)

	def get_max(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:PIN:MAX \n
		Sets the maximum value of the input power Pin. \n
			:return: pin_max: float Range: -145 to 20
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:PIN:MAX?')
		return Conversions.str_to_float(response)

	def set_max(self, pin_max: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:PIN:MAX \n
		Sets the maximum value of the input power Pin. \n
			:param pin_max: float Range: -145 to 20
		"""
		param = Conversions.decimal_value_to_str(pin_max)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:PIN:MAX {param}')

	def get_min(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:PIN:MIN \n
		Sets the minimum value of the input power Pin. \n
			:return: pin_min: float Range: -145 to 20
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:PIN:MIN?')
		return Conversions.str_to_float(response)

	def set_min(self, pin_min: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:PIN:MIN \n
		Sets the minimum value of the input power Pin. \n
			:param pin_min: float Range: -145 to 20
		"""
		param = Conversions.decimal_value_to_str(pin_min)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:PIN:MIN {param}')
