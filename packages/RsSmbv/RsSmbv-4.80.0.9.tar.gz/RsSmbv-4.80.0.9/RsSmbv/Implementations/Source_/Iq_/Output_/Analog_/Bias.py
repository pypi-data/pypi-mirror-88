from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bias:
	"""Bias commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bias", core, parent)

	def clone(self) -> 'Bias':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bias(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def coupling(self):
		"""coupling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coupling'):
			from .Bias_.Coupling import Coupling
			self._coupling = Coupling(self._core, self._base)
		return self._coupling

	def get_icomponent(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:BIAS:I \n
		Specifies the amplifier bias Vbias of the respective I or Q component. The value range is adjusted so that the maximum
		overall output voltage does not exceed 4V, see 'Maximum overall output voltage'. \n
			:return: ipart: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:BIAS:I?')
		return Conversions.str_to_float(response)

	def set_icomponent(self, ipart: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:BIAS:I \n
		Specifies the amplifier bias Vbias of the respective I or Q component. The value range is adjusted so that the maximum
		overall output voltage does not exceed 4V, see 'Maximum overall output voltage'. \n
			:param ipart: float Range: -3.6V to 3.6V , Unit: V
		"""
		param = Conversions.decimal_value_to_str(ipart)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:BIAS:I {param}')

	def get_qcomponent(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:BIAS:Q \n
		Specifies the amplifier bias Vbias of the respective I or Q component. The value range is adjusted so that the maximum
		overall output voltage does not exceed 4V, see 'Maximum overall output voltage'. \n
			:return: qpart: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:BIAS:Q?')
		return Conversions.str_to_float(response)

	def set_qcomponent(self, qpart: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:BIAS:Q \n
		Specifies the amplifier bias Vbias of the respective I or Q component. The value range is adjusted so that the maximum
		overall output voltage does not exceed 4V, see 'Maximum overall output voltage'. \n
			:param qpart: float Range: -3.6V to 3.6V , Unit: V
		"""
		param = Conversions.decimal_value_to_str(qpart)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:BIAS:Q {param}')
