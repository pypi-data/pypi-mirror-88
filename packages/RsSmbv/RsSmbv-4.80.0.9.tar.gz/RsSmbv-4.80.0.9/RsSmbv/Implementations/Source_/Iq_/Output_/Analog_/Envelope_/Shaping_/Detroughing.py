from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Detroughing:
	"""Detroughing commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("detroughing", core, parent)

	def get_coupling(self) -> bool:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:DETRoughing:COUPling \n
		Enables/disables deriving the detroughing factor (d) from the selected Vcc value. \n
			:return: coupling_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:DETRoughing:COUPling?')
		return Conversions.str_to_bool(response)

	def set_coupling(self, coupling_state: bool) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:DETRoughing:COUPling \n
		Enables/disables deriving the detroughing factor (d) from the selected Vcc value. \n
			:param coupling_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(coupling_state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:DETRoughing:COUPling {param}')

	def get_factor(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:DETRoughing:FACTor \n
		Sets the detroughing factor. \n
			:return: detr_factor: float Range: 0 to 2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:DETRoughing:FACTor?')
		return Conversions.str_to_float(response)

	def set_factor(self, detr_factor: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:DETRoughing:FACTor \n
		Sets the detroughing factor. \n
			:param detr_factor: float Range: 0 to 2
		"""
		param = Conversions.decimal_value_to_str(detr_factor)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:DETRoughing:FACTor {param}')

	# noinspection PyTypeChecker
	def get_function(self) -> enums.IqOutEnvDetrFunc:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:DETRoughing:FUNCtion \n
		Sets the detroughing function. \n
			:return: detr_function: F1| F2| F3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:DETRoughing:FUNCtion?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvDetrFunc)

	def set_function(self, detr_function: enums.IqOutEnvDetrFunc) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:DETRoughing:FUNCtion \n
		Sets the detroughing function. \n
			:param detr_function: F1| F2| F3
		"""
		param = Conversions.enum_scalar_to_str(detr_function, enums.IqOutEnvDetrFunc)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:DETRoughing:FUNCtion {param}')

	def get_pexponent(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:DETRoughing:PEXPonent \n
		Sets the exponent (a) for the detroughing function F3. \n
			:return: power_exponent: float Range: 1 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:DETRoughing:PEXPonent?')
		return Conversions.str_to_float(response)

	def set_pexponent(self, power_exponent: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:DETRoughing:PEXPonent \n
		Sets the exponent (a) for the detroughing function F3. \n
			:param power_exponent: float Range: 1 to 10
		"""
		param = Conversions.decimal_value_to_str(power_exponent)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:DETRoughing:PEXPonent {param}')
