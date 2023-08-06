from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Interleaver:
	"""Interleaver commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("interleaver", core, parent)

	def set(self, interleaver: bool, channel=repcap.Channel.Default, transportChannel=repcap.TransportChannel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:TCHannel<DI>:INTerleaver \n
		The command activates or deactivates channel coding interleaver state 1 for the selected channel. Interleaver state 1 can
		be activated and deactivated for each transport channel individually. The channel is selected via the suffix at TCHannel.
		Interleaver state 2 can only be activated or deactivated for all the transport channels together (method RsSmbv.Source.Bb.
		W3Gpp.Bstation.Enhanced.Channel.Dpch.Interleaver2.set) . Note: The interleaver states do not cause the symbol rate to
		change. \n
			:param interleaver: ON| OFF
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')"""
		param = Conversions.bool_to_str(interleaver)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:TCHannel{transportChannel_cmd_val}:INTerleaver {param}')

	def get(self, channel=repcap.Channel.Default, transportChannel=repcap.TransportChannel.Default) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:TCHannel<DI>:INTerleaver \n
		The command activates or deactivates channel coding interleaver state 1 for the selected channel. Interleaver state 1 can
		be activated and deactivated for each transport channel individually. The channel is selected via the suffix at TCHannel.
		Interleaver state 2 can only be activated or deactivated for all the transport channels together (method RsSmbv.Source.Bb.
		W3Gpp.Bstation.Enhanced.Channel.Dpch.Interleaver2.set) . Note: The interleaver states do not cause the symbol rate to
		change. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')
			:return: interleaver: ON| OFF"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:TCHannel{transportChannel_cmd_val}:INTerleaver?')
		return Conversions.str_to_bool(response)
