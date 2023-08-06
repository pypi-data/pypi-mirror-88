from typing import List

from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)

	def set(self, user: List[str], frameIx=repcap.FrameIx.Default, stream=repcap.Stream.Default, subchannel=repcap.Subchannel.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST>:[SUBChannel<US>]:[USER<CH>]:ETSC:USER \n
		(only for selection of burst type BB:GSM:SLOT:TYPE SYNC) The command selects an extended training sequence for the
		Synchronization burst USER sequence. \n
			:param user: integer
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.list_to_csv_str(user)
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{stream_cmd_val}:SUBChannel{subchannel_cmd_val}:USER{channel_cmd_val}:ETSC:USER {param}')

	def get(self, frameIx=repcap.FrameIx.Default, stream=repcap.Stream.Default, subchannel=repcap.Subchannel.Default, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:GSM:[FRAMe<DI>]:SLOT<ST>:[SUBChannel<US>]:[USER<CH>]:ETSC:USER \n
		(only for selection of burst type BB:GSM:SLOT:TYPE SYNC) The command selects an extended training sequence for the
		Synchronization burst USER sequence. \n
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubChannel')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: user: integer"""
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:SLOT{stream_cmd_val}:SUBChannel{subchannel_cmd_val}:USER{channel_cmd_val}:ETSC:USER?')
		return Conversions.str_to_str_list(response)
