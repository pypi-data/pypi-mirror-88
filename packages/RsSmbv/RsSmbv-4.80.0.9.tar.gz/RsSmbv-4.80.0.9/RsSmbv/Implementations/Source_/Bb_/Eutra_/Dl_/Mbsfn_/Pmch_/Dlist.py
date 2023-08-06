from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dlist:
	"""Dlist commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dlist", core, parent)

	def set(self, data_list: str, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH>:DLISt \n
		Sets the data list of the data source for the selected PMCH/MTCH. \n
			:param data_list: string
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmch')"""
		param = Conversions.value_to_quoted_str(data_list)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{channel_cmd_val}:DLISt {param}')

	def get(self, channel=repcap.Channel.Default) -> str:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH>:DLISt \n
		Sets the data list of the data source for the selected PMCH/MTCH. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmch')
			:return: data_list: string"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{channel_cmd_val}:DLISt?')
		return trim_str_response(response)
