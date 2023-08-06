from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Aone:
	"""Aone commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aone", core, parent)

	def clone(self) -> 'Aone':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Aone(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Aone_.Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def set(self, a_1: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SV:GPS<ST>:NMESsage:CNAV:TIME:CONVersion:UTC<CH>:AONE \n
		Sets the parameter A1. \n
			:param a_1: integer Range: -4096 to 4095
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Utc')"""
		param = Conversions.decimal_value_to_str(a_1)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:GPS{stream_cmd_val}:NMESsage:CNAV:TIME:CONVersion:UTC{channel_cmd_val}:AONE {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:SV:GPS<ST>:NMESsage:CNAV:TIME:CONVersion:UTC<CH>:AONE \n
		Sets the parameter A1. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Utc')
			:return: a_1: integer Range: -4096 to 4095"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:GPS{stream_cmd_val}:NMESsage:CNAV:TIME:CONVersion:UTC{channel_cmd_val}:AONE?')
		return Conversions.str_to_int(response)
