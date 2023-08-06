from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mccw:
	"""Mccw commands group definition. 41 total commands, 5 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mccw", core, parent)

	def clone(self) -> 'Mccw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mccw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def carrier(self):
		"""carrier commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_carrier'):
			from .Mccw_.Carrier import Carrier
			self._carrier = Carrier(self._core, self._base)
		return self._carrier

	@property
	def cfactor(self):
		"""cfactor commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_cfactor'):
			from .Mccw_.Cfactor import Cfactor
			self._cfactor = Cfactor(self._core, self._base)
		return self._cfactor

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_clock'):
			from .Mccw_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def edit(self):
		"""edit commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_edit'):
			from .Mccw_.Edit import Edit
			self._edit = Edit(self._core, self._base)
		return self._edit

	@property
	def trigger(self):
		"""trigger commands group. 4 Sub-classes, 4 commands."""
		if not hasattr(self, '_trigger'):
			from .Mccw_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:MCCW:PRESet \n
		Sets all multi carrier signal parameters to their default values. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:MCCW:PRESet \n
		Sets all multi carrier signal parameters to their default values. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:MCCW:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:MCCW:STATe \n
		Enables/disables the multi carrier CW signal. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:MCCW:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:MCCW:STATe \n
		Enables/disables the multi carrier CW signal. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:STATe {param}')
