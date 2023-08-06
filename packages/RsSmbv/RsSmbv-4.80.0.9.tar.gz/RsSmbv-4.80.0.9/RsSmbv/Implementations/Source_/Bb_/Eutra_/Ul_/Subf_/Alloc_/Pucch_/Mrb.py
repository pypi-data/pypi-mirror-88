from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mrb:
	"""Mrb commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mrb", core, parent)

	def set(self, pucch_mrb: enums.NumbersC, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:ALLoc<CH>:PUCCh:MRB \n
		Sets the number of resource blocks used by PUCCH format 5. \n
			:param pucch_mrb: 1| 2| 3| 4| 5| 6| 8
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(pucch_mrb, enums.NumbersC)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUCCh:MRB {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.NumbersC:
		"""[SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:ALLoc<CH>:PUCCh:MRB \n
		Sets the number of resource blocks used by PUCCH format 5. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: pucch_mrb: 1| 2| 3| 4| 5| 6| 8"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUCCh:MRB?')
		return Conversions.str_to_scalar_enum(response, enums.NumbersC)
