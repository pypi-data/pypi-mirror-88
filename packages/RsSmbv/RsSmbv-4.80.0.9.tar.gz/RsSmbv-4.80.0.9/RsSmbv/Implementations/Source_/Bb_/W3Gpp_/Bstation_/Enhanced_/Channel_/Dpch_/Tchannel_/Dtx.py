from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dtx:
	"""Dtx commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dtx", core, parent)

	def set(self, dtx: int, channel=repcap.Channel.Default, transportChannel=repcap.TransportChannel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:TCHannel<DI>:DTX \n
		The command sets the number of DTX (Discontinuous Transmission) bits. These bits are entered in the data stream between
		rate matching and interleaver 1 and used for the BTFD reference measurement channels rate 2 and rate 3. \n
			:param dtx: integer Range: 0 to 1024
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')"""
		param = Conversions.decimal_value_to_str(dtx)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:TCHannel{transportChannel_cmd_val}:DTX {param}')

	def get(self, channel=repcap.Channel.Default, transportChannel=repcap.TransportChannel.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:TCHannel<DI>:DTX \n
		The command sets the number of DTX (Discontinuous Transmission) bits. These bits are entered in the data stream between
		rate matching and interleaver 1 and used for the BTFD reference measurement channels rate 2 and rate 3. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')
			:return: dtx: integer Range: 0 to 1024"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:TCHannel{transportChannel_cmd_val}:DTX?')
		return Conversions.str_to_int(response)
