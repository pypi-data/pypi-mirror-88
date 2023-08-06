from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmr1:
	"""Dmr1 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dmr1", core, parent)

	def set(self, pucc_dmrs_1: enums.EutraPuccN1Dmrs, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:ALLoc<CH>:PUCCh:DMR1 \n
		Sets the index n(2) DMRS. \n
			:param pucc_dmrs_1: 0| 2| 3| 4| 6| 8| 9| 10
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(pucc_dmrs_1, enums.EutraPuccN1Dmrs)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUCCh:DMR1 {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EutraPuccN1Dmrs:
		"""[SOURce<HW>]:BB:EUTRa:UL:[SUBF<ST>]:ALLoc<CH>:PUCCh:DMR1 \n
		Sets the index n(2) DMRS. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: pucc_dmrs_1: 0| 2| 3| 4| 6| 8| 9| 10"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:SUBF{stream_cmd_val}:ALLoc{channel_cmd_val}:PUCCh:DMR1?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPuccN1Dmrs)
