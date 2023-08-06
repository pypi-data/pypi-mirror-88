from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RuIndicator:
	"""RuIndicator commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ruIndicator", core, parent)

	def set(self, ruin: str, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:FDB<ST>:RUINdicator \n
		Sets the route indicator. \n
			:param ruin: a single upper case alphabetic character Allowed are letters, excluding “I” and “O”, or the “space” character.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fdb')"""
		param = Conversions.value_to_quoted_str(ruin)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:FDB{stream_cmd_val}:RUINdicator {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> str:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:FDB<ST>:RUINdicator \n
		Sets the route indicator. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fdb')
			:return: ruin: a single upper case alphabetic character Allowed are letters, excluding “I” and “O”, or the “space” character."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:FDB{stream_cmd_val}:RUINdicator?')
		return trim_str_response(response)
