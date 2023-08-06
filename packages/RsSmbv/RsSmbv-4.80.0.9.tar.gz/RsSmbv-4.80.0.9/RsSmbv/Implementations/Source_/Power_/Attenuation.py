from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Attenuation:
	"""Attenuation commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("attenuation", core, parent)

	def clone(self) -> 'Attenuation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Attenuation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def rfOff(self):
		"""rfOff commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfOff'):
			from .Attenuation_.RfOff import RfOff
			self._rfOff = RfOff(self._core, self._base)
		return self._rfOff

	def get_digital(self) -> float:
		"""[SOURce<HW>]:POWer:ATTenuation:DIGital \n
		Sets a relative attenuation value for the baseband signal. \n
			:return: att_digital: float Range: -3.522 to 80
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ATTenuation:DIGital?')
		return Conversions.str_to_float(response)

	def set_digital(self, att_digital: float) -> None:
		"""[SOURce<HW>]:POWer:ATTenuation:DIGital \n
		Sets a relative attenuation value for the baseband signal. \n
			:param att_digital: float Range: -3.522 to 80
		"""
		param = Conversions.decimal_value_to_str(att_digital)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ATTenuation:DIGital {param}')

	def get_stage(self) -> float:
		"""[SOURce<HW>]:POWer:ATTenuation:STAGe \n
		No command help available \n
			:return: stage: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ATTenuation:STAGe?')
		return Conversions.str_to_float(response)
