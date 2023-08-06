from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mcode:
	"""Mcode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcode", core, parent)

	def set(self, mcode: bool, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:DPCCh:MCODe \n
		The command activates multicode transmission for the selected channel (ON) or deactivates it (OFF) . The multicode
		channels are destined for the same receiver, that is to say, are part of a radio link. The first channel of this group is
		used as the master channel. The common components (Pilot, TPC and TCFI) for all the channels are then spread using the
		spreading code of the master channel. \n
			:param mcode: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.bool_to_str(mcode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:DPCCh:MCODe {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:DPCCh:MCODe \n
		The command activates multicode transmission for the selected channel (ON) or deactivates it (OFF) . The multicode
		channels are destined for the same receiver, that is to say, are part of a radio link. The first channel of this group is
		used as the master channel. The common components (Pilot, TPC and TCFI) for all the channels are then spread using the
		spreading code of the master channel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: mcode: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:DPCCh:MCODe?')
		return Conversions.str_to_bool(response)
