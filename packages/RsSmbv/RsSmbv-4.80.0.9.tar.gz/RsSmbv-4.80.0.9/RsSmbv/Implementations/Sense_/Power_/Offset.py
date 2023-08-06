from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Offset:
	"""Offset commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("offset", core, parent)

	def clone(self) -> 'Offset':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Offset(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Offset_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def set(self, offset: float, channel=repcap.Channel.Default) -> None:
		"""SENSe<CH>:[POWer]:OFFSet \n
		Sets a level offset which is added to the measured level value after activation with command OFFSet:STATe. The level
		offset allows, e.g. to consider an attenuator in the signal path. \n
			:param offset: float Range: -100.0 to 100.0, Unit: dB
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		param = Conversions.decimal_value_to_str(offset)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:OFFSet {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SENSe<CH>:[POWer]:OFFSet \n
		Sets a level offset which is added to the measured level value after activation with command OFFSet:STATe. The level
		offset allows, e.g. to consider an attenuator in the signal path. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: offset: float Range: -100.0 to 100.0, Unit: dB"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:OFFSet?')
		return Conversions.str_to_float(response)
