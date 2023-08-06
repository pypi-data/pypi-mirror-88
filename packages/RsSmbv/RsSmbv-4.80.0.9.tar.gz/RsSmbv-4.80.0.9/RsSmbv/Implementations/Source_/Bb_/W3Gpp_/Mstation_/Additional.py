from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Additional:
	"""Additional commands group definition. 5 total commands, 3 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("additional", core, parent)

	def clone(self) -> 'Additional':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Additional(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Additional_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def scode(self):
		"""scode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scode'):
			from .Additional_.Scode import Scode
			self._scode = Scode(self._core, self._base)
		return self._scode

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Additional_.Tdelay import Tdelay
			self._tdelay = Tdelay(self._core, self._base)
		return self._tdelay

	def get_count(self) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:COUNt \n
		The command sets the amount of additional user equipment. Up to 128 additional user equipment can be simulated -
		corresponding to a receive signal for a base station with high capacity utilization. The fourth user equipment (UE4)
		serves as a template for all other stations. The only parameters of the additional user equipment to be modified are the
		scrambling code and the power. \n
			:return: count: integer Range: 1 to 128
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, count: int) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:COUNt \n
		The command sets the amount of additional user equipment. Up to 128 additional user equipment can be simulated -
		corresponding to a receive signal for a base station with high capacity utilization. The fourth user equipment (UE4)
		serves as a template for all other stations. The only parameters of the additional user equipment to be modified are the
		scrambling code and the power. \n
			:param count: integer Range: 1 to 128
		"""
		param = Conversions.decimal_value_to_str(count)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:COUNt {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:STATe \n
		Activates additional user equipment. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:STATe \n
		Activates additional user equipment. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:STATe {param}')
