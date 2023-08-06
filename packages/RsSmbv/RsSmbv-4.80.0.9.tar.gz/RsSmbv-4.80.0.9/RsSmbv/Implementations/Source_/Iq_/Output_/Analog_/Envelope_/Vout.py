from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vout:
	"""Vout commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vout", core, parent)

	def get_max(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VOUT:MAX \n
		Queries the minimum and maximum values of the estimated envelope output voltage Vout. \n
			:return: vout_max: float Range: 0.04 to 8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VOUT:MAX?')
		return Conversions.str_to_float(response)

	def set_max(self, vout_max: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VOUT:MAX \n
		Queries the minimum and maximum values of the estimated envelope output voltage Vout. \n
			:param vout_max: float Range: 0.04 to 8
		"""
		param = Conversions.decimal_value_to_str(vout_max)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VOUT:MAX {param}')

	def get_min(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VOUT:MIN \n
		Queries the minimum and maximum values of the estimated envelope output voltage Vout. \n
			:return: vout_min: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VOUT:MIN?')
		return Conversions.str_to_float(response)

	def set_min(self, vout_min: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VOUT:MIN \n
		Queries the minimum and maximum values of the estimated envelope output voltage Vout. \n
			:param vout_min: float Range: 0.04 to 8
		"""
		param = Conversions.decimal_value_to_str(vout_min)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VOUT:MIN {param}')
