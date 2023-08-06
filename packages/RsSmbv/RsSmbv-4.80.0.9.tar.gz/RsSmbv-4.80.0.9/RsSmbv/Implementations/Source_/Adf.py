from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Adf:
	"""Adf commands group definition. 17 total commands, 3 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("adf", core, parent)

	def clone(self) -> 'Adf':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Adf(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Adf_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_setting'):
			from .Adf_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def trigger(self):
		"""trigger commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_trigger'):
			from .Adf_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def preset(self) -> None:
		"""[SOURce<HW>]:ADF:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:ADF:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:ADF:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:ADF:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:ADF:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ADF:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:ADF:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:ADF:STATe {param}')
