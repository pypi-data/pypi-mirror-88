from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sflist:
	"""Sflist commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sflist", core, parent)

	def get(self, channel=repcap.Channel.Default) -> str:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:ALLoc<CH>:SFList \n
		Queries the subframes in that the channel is allocated. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: subframe_list: 'SF#, SF#, SF#, SF#...' String of four comma-separated integer values, indicating subframe numbers"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:ALLoc{channel_cmd_val}:SFList?')
		return trim_str_response(response)
