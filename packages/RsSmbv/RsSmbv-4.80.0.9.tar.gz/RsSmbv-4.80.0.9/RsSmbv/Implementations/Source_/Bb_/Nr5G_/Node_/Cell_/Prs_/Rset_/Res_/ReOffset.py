from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReOffset:
	"""ReOffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("reOffset", core, parent)

	def set(self, prs_res_re_off: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:RES<DIR>:REOFfset \n
		Sets the resource element (RE) offset in the frequency domain for the first symbol in a resource. \n
			:param prs_res_re_off: integer Range: 0 to E_IdNr5gPrsCombSize_MAX-1
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')"""
		param = Conversions.decimal_value_to_str(prs_res_re_off)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:REOFfset {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default) -> int:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:RES<DIR>:REOFfset \n
		Sets the resource element (RE) offset in the frequency domain for the first symbol in a resource. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:return: prs_res_re_off: integer Range: 0 to E_IdNr5gPrsCombSize_MAX-1"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:REOFfset?')
		return Conversions.str_to_int(response)
