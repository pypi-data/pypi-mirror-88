from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Azero:
	"""Azero commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("azero", core, parent)

	def clone(self) -> 'Azero':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Azero(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Azero_.Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def set(self, a_0: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SV:GPS<ST>:NMESsage:CNAV:TIME:CONVersion:GLONass<CH>:AZERo \n
		No command help available \n
			:param a_0: integer Range: -32768 to 32767
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')"""
		param = Conversions.decimal_value_to_str(a_0)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:GPS{stream_cmd_val}:NMESsage:CNAV:TIME:CONVersion:GLONass{channel_cmd_val}:AZERo {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:SV:GPS<ST>:NMESsage:CNAV:TIME:CONVersion:GLONass<CH>:AZERo \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:return: a_0: integer Range: -32768 to 32767"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:GPS{stream_cmd_val}:NMESsage:CNAV:TIME:CONVersion:GLONass{channel_cmd_val}:AZERo?')
		return Conversions.str_to_int(response)
