from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unscaled:
	"""Unscaled commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("unscaled", core, parent)

	def set(self, af: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default, gnssIndex=repcap.GnssIndex.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:NMESsage:NAV:CCORrection:AF<S2US>:UNSCaled \n
		Sets the parameter AF 0 to 2. \n
			:param af: integer
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:param gnssIndex: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Af')"""
		param = Conversions.decimal_value_to_str(af)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		gnssIndex_cmd_val = self._base.get_repcap_cmd_value(gnssIndex, repcap.GnssIndex)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:NMESsage:NAV:CCORrection:AF{gnssIndex_cmd_val}:UNSCaled {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, gnssIndex=repcap.GnssIndex.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:NMESsage:NAV:CCORrection:AF<S2US>:UNSCaled \n
		Sets the parameter AF 0 to 2. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:param gnssIndex: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Af')
			:return: af: integer"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		gnssIndex_cmd_val = self._base.get_repcap_cmd_value(gnssIndex, repcap.GnssIndex)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:NMESsage:NAV:CCORrection:AF{gnssIndex_cmd_val}:UNSCaled?')
		return Conversions.str_to_int(response)
