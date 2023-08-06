from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sqid:
	"""Sqid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sqid", core, parent)

	def set(self, prs_res_seq_id: int, channel=repcap.Channel.Default, stream=repcap.Stream.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:RES<DIR>:SQID \n
		Sets the resource ID to initialize the cinit value for the generation of the DL PRS sequence. \n
			:param prs_res_seq_id: integer Range: 0 to 4095
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')"""
		param = Conversions.decimal_value_to_str(prs_res_seq_id)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:SQID {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, srsRsrcSetRsrc=repcap.SrsRsrcSetRsrc.Default) -> int:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:RES<DIR>:SQID \n
		Sets the resource ID to initialize the cinit value for the generation of the DL PRS sequence. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:param srsRsrcSetRsrc: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Res')
			:return: prs_res_seq_id: integer Range: 0 to 4095"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		srsRsrcSetRsrc_cmd_val = self._base.get_repcap_cmd_value(srsRsrcSetRsrc, repcap.SrsRsrcSetRsrc)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:RES{srsRsrcSetRsrc_cmd_val}:SQID?')
		return Conversions.str_to_int(response)
