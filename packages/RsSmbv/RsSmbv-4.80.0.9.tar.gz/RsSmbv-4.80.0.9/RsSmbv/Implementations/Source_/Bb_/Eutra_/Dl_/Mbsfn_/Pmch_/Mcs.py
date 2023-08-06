from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mcs:
	"""Mcs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcs", core, parent)

	def set(self, mcs: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH>:MCS \n
		Sets the modulation and coding scheme (MCS) applicable for the subframes of the (P) MCH. \n
			:param mcs: integer Range: 0 to 28
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmch')"""
		param = Conversions.decimal_value_to_str(mcs)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{channel_cmd_val}:MCS {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH>:MCS \n
		Sets the modulation and coding scheme (MCS) applicable for the subframes of the (P) MCH. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmch')
			:return: mcs: integer Range: 0 to 28"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{channel_cmd_val}:MCS?')
		return Conversions.str_to_int(response)
