from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tot:
	"""Tot commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tot", core, parent)

	def clone(self) -> 'Tot':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tot(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def unscaled(self):
		"""unscaled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unscaled'):
			from .Tot_.Unscaled import Unscaled
			self._unscaled = Unscaled(self._core, self._base)
		return self._unscaled

	def set(self, tot: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SV:NAVic<ST>:NMESsage:NAV:TIME:CONVersion:GPS<CH>:TOT \n
		Sets the Tot parameter. \n
			:param tot: integer Range: 0 to 65535
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.decimal_value_to_str(tot)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:NAVic{stream_cmd_val}:NMESsage:NAV:TIME:CONVersion:GPS{channel_cmd_val}:TOT {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:SV:NAVic<ST>:NMESsage:NAV:TIME:CONVersion:GPS<CH>:TOT \n
		Sets the Tot parameter. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: tot: integer Range: 0 to 65535"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:NAVic{stream_cmd_val}:NMESsage:NAV:TIME:CONVersion:GPS{channel_cmd_val}:TOT?')
		return Conversions.str_to_int(response)
