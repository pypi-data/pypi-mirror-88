from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Use:
	"""Use commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("use", core, parent)

	def set(self, use: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:SCRambling:CELL<ST>:DMRS:USE \n
		Defines how the DMRS scrambling sequence is initialized. \n
			:param use: 0| 1| OFF| ON OFF DRMS sequence is generated with the variable nID = NIDcell. ON Used are two variable nID = nIDDMRS,i set with the commands [:SOURcehw]:BB:EUTRa:DL:USERch:SCRambling:CELLst:DMRS:ID1|ID2
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.bool_to_str(use)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:SCRambling:CELL{stream_cmd_val}:DMRS:USE {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:SCRambling:CELL<ST>:DMRS:USE \n
		Defines how the DMRS scrambling sequence is initialized. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: use: 0| 1| OFF| ON OFF DRMS sequence is generated with the variable nID = NIDcell. ON Used are two variable nID = nIDDMRS,i set with the commands [:SOURcehw]:BB:EUTRa:DL:USERch:SCRambling:CELLst:DMRS:ID1|ID2"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:SCRambling:CELL{stream_cmd_val}:DMRS:USE?')
		return Conversions.str_to_bool(response)
