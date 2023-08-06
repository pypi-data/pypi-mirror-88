from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SaEnd:
	"""SaEnd commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("saEnd", core, parent)

	def set(self, alloc_end: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH>:SAENd \n
		Defines the first/last subframe allocated to this (P) MCH within a period identified by field commonSF-Alloc. \n
			:param alloc_end: integer Range: 0 to 1535
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmch')"""
		param = Conversions.decimal_value_to_str(alloc_end)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{channel_cmd_val}:SAENd {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH>:SAENd \n
		Defines the first/last subframe allocated to this (P) MCH within a period identified by field commonSF-Alloc. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmch')
			:return: alloc_end: integer Range: 0 to 1535"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{channel_cmd_val}:SAENd?')
		return Conversions.str_to_int(response)
