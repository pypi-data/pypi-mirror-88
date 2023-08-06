from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rid:
	"""Rid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rid", core, parent)

	def set(self, rid: str, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:RID \n
		Sets the GBAS ID. \n
			:param rid: string A four-character (24-bit) alphanumeric field that identifies the ground station broadcasting the message. Permitted are capital letter, numbers and 'space'.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.value_to_quoted_str(rid)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:RID {param}')

	def get(self, channel=repcap.Channel.Default) -> str:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:RID \n
		Sets the GBAS ID. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: rid: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:RID?')
		return trim_str_response(response)
