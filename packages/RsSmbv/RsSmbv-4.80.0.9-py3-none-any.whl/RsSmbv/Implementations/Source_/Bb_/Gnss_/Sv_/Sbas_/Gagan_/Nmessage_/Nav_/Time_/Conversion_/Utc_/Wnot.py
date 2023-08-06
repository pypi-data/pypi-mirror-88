from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Wnot:
	"""Wnot commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("wnot", core, parent)

	def set(self, wnot: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SV:SBAS<ST>:GAGAN:NMESsage:NAV:TIME:CONVersion:UTC<CH>:WNOT \n
		Sets the parameter WNot. \n
			:param wnot: integer Range: 0 to 529947
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Utc')"""
		param = Conversions.decimal_value_to_str(wnot)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:SBAS{stream_cmd_val}:GAGAN:NMESsage:NAV:TIME:CONVersion:UTC{channel_cmd_val}:WNOT {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:SV:SBAS<ST>:GAGAN:NMESsage:NAV:TIME:CONVersion:UTC<CH>:WNOT \n
		Sets the parameter WNot. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Utc')
			:return: wnot: integer Range: 0 to 529947"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:SBAS{stream_cmd_val}:GAGAN:NMESsage:NAV:TIME:CONVersion:UTC{channel_cmd_val}:WNOT?')
		return Conversions.str_to_int(response)
