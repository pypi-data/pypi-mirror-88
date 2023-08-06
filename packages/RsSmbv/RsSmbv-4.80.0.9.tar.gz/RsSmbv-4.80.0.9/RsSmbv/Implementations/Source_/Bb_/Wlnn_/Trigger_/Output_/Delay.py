from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 4 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	def clone(self) -> 'Delay':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Delay(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def maximum(self):
		"""maximum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_maximum'):
			from .Delay_.Maximum import Maximum
			self._maximum = Maximum(self._core, self._base)
		return self._maximum

	@property
	def minimum(self):
		"""minimum commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_minimum'):
			from .Delay_.Minimum import Minimum
			self._minimum = Minimum(self._core, self._base)
		return self._minimum

	def set(self, delay: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:OUTPut<CH>:DELay \n
		Defines the delay between the signal on the marker outputs and the start of the signals. \n
			:param delay: float Range: 0 to 16777215
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(delay)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:TRIGger:OUTPut{channel_cmd_val}:DELay {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:OUTPut<CH>:DELay \n
		Defines the delay between the signal on the marker outputs and the start of the signals. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: delay: float Range: 0 to 16777215"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:TRIGger:OUTPut{channel_cmd_val}:DELay?')
		return Conversions.str_to_float(response)

	def get_fixed(self) -> bool:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:OUTPut:DELay:FIXed \n
		No command help available \n
			:return: fixed: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:TRIGger:OUTPut:DELay:FIXed?')
		return Conversions.str_to_bool(response)

	def set_fixed(self, fixed: bool) -> None:
		"""[SOURce<HW>]:BB:WLNN:TRIGger:OUTPut:DELay:FIXed \n
		No command help available \n
			:param fixed: No help available
		"""
		param = Conversions.bool_to_str(fixed)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:TRIGger:OUTPut:DELay:FIXed {param}')
