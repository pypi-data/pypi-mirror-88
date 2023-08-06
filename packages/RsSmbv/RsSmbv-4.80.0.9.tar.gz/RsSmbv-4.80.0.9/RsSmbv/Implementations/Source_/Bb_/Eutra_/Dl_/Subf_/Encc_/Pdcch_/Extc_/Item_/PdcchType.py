from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PdcchType:
	"""PdcchType commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pdcchType", core, parent)

	def set(self, pdcch_type: enums.EutraPdcchType, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:PDCChtype \n
		Sets if the DCI is carried by a PDCCH or by an EPDCCH set. \n
			:param pdcch_type: PDCCh| EPD1| EPD2 EPD1|EPD2 EPDCCH sets cannot be allocated TDD special subframes, if the combinations listed in Table 'Combinations of cyclic prefix and TDD special subframe configurations' apply.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')"""
		param = Conversions.enum_scalar_to_str(pdcch_type, enums.EutraPdcchType)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:PDCChtype {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EutraPdcchType:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:PDCChtype \n
		Sets if the DCI is carried by a PDCCH or by an EPDCCH set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')
			:return: pdcch_type: PDCCh| EPD1| EPD2 EPD1|EPD2 EPDCCH sets cannot be allocated TDD special subframes, if the combinations listed in Table 'Combinations of cyclic prefix and TDD special subframe configurations' apply."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:PDCChtype?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPdcchType)
