from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ...........Internal.Utilities import trim_str_response
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pattern:
	"""Pattern commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pattern", core, parent)

	def set(self, pattern: str, stream=repcap.Stream.Default, channel=repcap.Channel.Default, subchannel=repcap.Subchannel.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:SLOT<CH>:CHANnel<US>:DPCCh:SYNC:PATTern \n
		Sets the bit pattern for the sync shift. \n
			:param pattern: string The maximum pattern length is 64 bits.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.value_to_quoted_str(pattern)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:CHANnel{subchannel_cmd_val}:DPCCh:SYNC:PATTern {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default, subchannel=repcap.Subchannel.Default) -> str:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:SLOT<CH>:CHANnel<US>:DPCCh:SYNC:PATTern \n
		Sets the bit pattern for the sync shift. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:param subchannel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: pattern: string The maximum pattern length is 64 bits."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		subchannel_cmd_val = self._base.get_repcap_cmd_value(subchannel, repcap.Subchannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:CHANnel{subchannel_cmd_val}:DPCCh:SYNC:PATTern?')
		return trim_str_response(response)
