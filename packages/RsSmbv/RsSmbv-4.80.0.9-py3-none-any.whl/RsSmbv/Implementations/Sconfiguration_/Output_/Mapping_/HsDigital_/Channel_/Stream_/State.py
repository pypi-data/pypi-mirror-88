from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""SCONfiguration:OUTPut:MAPPing:HSDigital<CH>:CHANnel:STReam<ST>:STATe \n
		Maps the I/Q output streams to the output connectors. \n
			:param state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'HsDigital')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.bool_to_str(state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SCONfiguration:OUTPut:MAPPing:HSDigital{channel_cmd_val}:CHANnel:STReam{stream_cmd_val}:STATe {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""SCONfiguration:OUTPut:MAPPing:HSDigital<CH>:CHANnel:STReam<ST>:STATe \n
		Maps the I/Q output streams to the output connectors. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'HsDigital')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SCONfiguration:OUTPut:MAPPing:HSDigital{channel_cmd_val}:CHANnel:STReam{stream_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
