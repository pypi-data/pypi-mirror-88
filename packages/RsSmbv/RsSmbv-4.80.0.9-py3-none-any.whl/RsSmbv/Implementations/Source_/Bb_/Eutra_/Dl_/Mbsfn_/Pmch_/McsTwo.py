from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McsTwo:
	"""McsTwo commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcsTwo", core, parent)

	def set(self, pmch_mcs_two: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH>:MCSTwo \n
		Defines which of the two tables defined in is used to specify the used modulation and coding scheme. \n
			:param pmch_mcs_two: 0| 1| OFF| ON 0 Table 7.1.7.1-1 is used 1 Table 7.1.7.1-1A is used
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmch')"""
		param = Conversions.bool_to_str(pmch_mcs_two)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{channel_cmd_val}:MCSTwo {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:PMCH<CH>:MCSTwo \n
		Defines which of the two tables defined in is used to specify the used modulation and coding scheme. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Pmch')
			:return: pmch_mcs_two: 0| 1| OFF| ON 0 Table 7.1.7.1-1 is used 1 Table 7.1.7.1-1A is used"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:PMCH{channel_cmd_val}:MCSTwo?')
		return Conversions.str_to_bool(response)
