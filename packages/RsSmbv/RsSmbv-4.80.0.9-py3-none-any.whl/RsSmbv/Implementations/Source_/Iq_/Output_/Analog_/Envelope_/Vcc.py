from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vcc:
	"""Vcc commands group definition. 5 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vcc", core, parent)

	def clone(self) -> 'Vcc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Vcc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def value(self):
		"""value commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_value'):
			from .Vcc_.Value import Value
			self._value = Value(self._core, self._base)
		return self._value

	def get_max(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VCC:MAX \n
		Sets the maximum value of the supply voltage Vcc. \n
			:return: vcc_max: float Range: 0.04 to 8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VCC:MAX?')
		return Conversions.str_to_float(response)

	def set_max(self, vcc_max: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VCC:MAX \n
		Sets the maximum value of the supply voltage Vcc. \n
			:param vcc_max: float Range: 0.04 to 8
		"""
		param = Conversions.decimal_value_to_str(vcc_max)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VCC:MAX {param}')

	def get_min(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VCC:MIN \n
		Sets the maximum value of the supply voltage Vcc. \n
			:return: vcc_min: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VCC:MIN?')
		return Conversions.str_to_float(response)

	def set_min(self, vcc_min: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VCC:MIN \n
		Sets the maximum value of the supply voltage Vcc. \n
			:param vcc_min: float Range: 0.04 to 8
		"""
		param = Conversions.decimal_value_to_str(vcc_min)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VCC:MIN {param}')

	def get_offset(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VCC:OFFSet \n
		Applies a voltage offset on the supply voltage Vcc. \n
			:return: vcc_offset: float Range: 0 to 30, Unit: mV
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VCC:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, vcc_offset: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VCC:OFFSet \n
		Applies a voltage offset on the supply voltage Vcc. \n
			:param vcc_offset: float Range: 0 to 30, Unit: mV
		"""
		param = Conversions.decimal_value_to_str(vcc_offset)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VCC:OFFSet {param}')
