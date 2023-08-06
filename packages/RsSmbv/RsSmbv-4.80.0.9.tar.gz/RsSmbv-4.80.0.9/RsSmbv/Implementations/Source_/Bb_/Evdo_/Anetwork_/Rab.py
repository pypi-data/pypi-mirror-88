from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rab:
	"""Rab commands group definition. 5 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rab", core, parent)

	def clone(self) -> 'Rab':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rab(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mac(self):
		"""mac commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mac'):
			from .Rab_.Mac import Mac
			self._mac = Mac(self._core, self._base)
		return self._mac

	# noinspection PyTypeChecker
	def get_length(self) -> enums.EvdoRabLen:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:RAB:LENGth \n
		Sets the duration (in slots) of a Reverse Activity bit. Note: This parameter is available for physical layer subtype 0&1
		only. \n
			:return: length: RL8| RL16| RL32| RL64
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:ANETwork:RAB:LENGth?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoRabLen)

	def set_length(self, length: enums.EvdoRabLen) -> None:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:RAB:LENGth \n
		Sets the duration (in slots) of a Reverse Activity bit. Note: This parameter is available for physical layer subtype 0&1
		only. \n
			:param length: RL8| RL16| RL32| RL64
		"""
		param = Conversions.enum_scalar_to_str(length, enums.EvdoRabLen)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:ANETwork:RAB:LENGth {param}')

	def get_level(self) -> float:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:RAB:LEVel \n
		Sets the power within the MAC block for the Reverse Activity channel. \n
			:return: level: float Range: -25 to -7
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:ANETwork:RAB:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:RAB:LEVel \n
		Sets the power within the MAC block for the Reverse Activity channel. \n
			:param level: float Range: -25 to -7
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:ANETwork:RAB:LEVel {param}')

	def get_offset(self) -> int:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:RAB:OFFSet \n
		Sets the starting time offset of the Reverse Activity bit in slots. The command is specified in Reverse Activity Length/8
		units. The RA bit starts when the following equation is satisfied: System Time mod RAB length = RAB Offset, where System
		Time is expressed in slots. Note: This parameter is available for physical layer subtype 0&1 only. \n
			:return: offset: integer Range: 0 to 7
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:ANETwork:RAB:OFFSet?')
		return Conversions.str_to_int(response)

	def set_offset(self, offset: int) -> None:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:RAB:OFFSet \n
		Sets the starting time offset of the Reverse Activity bit in slots. The command is specified in Reverse Activity Length/8
		units. The RA bit starts when the following equation is satisfied: System Time mod RAB length = RAB Offset, where System
		Time is expressed in slots. Note: This parameter is available for physical layer subtype 0&1 only. \n
			:param offset: integer Range: 0 to 7
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:ANETwork:RAB:OFFSet {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:RAB:STATe \n
		Activates or deactivates the reverse activity bit (RAB) . \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:ANETwork:RAB:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:EVDO:ANETwork:RAB:STATe \n
		Activates or deactivates the reverse activity bit (RAB) . \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:ANETwork:RAB:STATe {param}')
