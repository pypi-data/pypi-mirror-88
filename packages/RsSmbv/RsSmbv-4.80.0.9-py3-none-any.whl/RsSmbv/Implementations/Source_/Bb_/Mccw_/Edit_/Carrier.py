from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Carrier:
	"""Carrier commands group definition. 8 total commands, 3 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("carrier", core, parent)

	def clone(self) -> 'Carrier':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Carrier(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Carrier_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def phase(self):
		"""phase commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_phase'):
			from .Carrier_.Phase import Phase
			self._phase = Phase(self._core, self._base)
		return self._phase

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Carrier_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	def get_start(self) -> int:
		"""[SOURce<HW>]:BB:MCCW:EDIT:CARRier:STARt \n
		Defines the first/last carrier in the carrier range to which joint configuration applies. \n
			:return: start: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:MCCW:EDIT:CARRier:STARt?')
		return Conversions.str_to_int(response)

	def set_start(self, start: int) -> None:
		"""[SOURce<HW>]:BB:MCCW:EDIT:CARRier:STARt \n
		Defines the first/last carrier in the carrier range to which joint configuration applies. \n
			:param start: integer Range: 0 to 8191
		"""
		param = Conversions.decimal_value_to_str(start)
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:EDIT:CARRier:STARt {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:MCCW:EDIT:CARRier:STATe \n
		Switches all the carriers in the selected carrier range on or off. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:MCCW:EDIT:CARRier:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:MCCW:EDIT:CARRier:STATe \n
		Switches all the carriers in the selected carrier range on or off. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:EDIT:CARRier:STATe {param}')

	def get_stop(self) -> int:
		"""[SOURce<HW>]:BB:MCCW:EDIT:CARRier:STOP \n
		Defines the first/last carrier in the carrier range to which joint configuration applies. \n
			:return: stop: integer Range: 0 to 8191
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:MCCW:EDIT:CARRier:STOP?')
		return Conversions.str_to_int(response)

	def set_stop(self, stop: int) -> None:
		"""[SOURce<HW>]:BB:MCCW:EDIT:CARRier:STOP \n
		Defines the first/last carrier in the carrier range to which joint configuration applies. \n
			:param stop: integer Range: 0 to 8191
		"""
		param = Conversions.decimal_value_to_str(stop)
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:EDIT:CARRier:STOP {param}')
