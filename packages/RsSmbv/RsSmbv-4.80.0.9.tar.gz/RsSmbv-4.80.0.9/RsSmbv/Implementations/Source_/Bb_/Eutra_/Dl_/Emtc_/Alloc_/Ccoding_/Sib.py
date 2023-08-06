from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sib:
	"""Sib commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sib", core, parent)

	def set(self, scheduling_sib_1: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:CCODing:SIB \n
		Sets the parameter schedulingInfoSIB1-RB and defines the PDSCH number of repetitions. Query the resulting number of
		repetitions with the command method RsSmbv.Source.Bb.Eutra.Dl.Emtc.Alloc.Ccoding.Rsib.get_. \n
			:param scheduling_sib_1: integer Range: 0 to 18
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.decimal_value_to_str(scheduling_sib_1)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:CCODing:SIB {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:CCODing:SIB \n
		Sets the parameter schedulingInfoSIB1-RB and defines the PDSCH number of repetitions. Query the resulting number of
		repetitions with the command method RsSmbv.Source.Bb.Eutra.Dl.Emtc.Alloc.Ccoding.Rsib.get_. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: scheduling_sib_1: integer Range: 0 to 18"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:CCODing:SIB?')
		return Conversions.str_to_int(response)
