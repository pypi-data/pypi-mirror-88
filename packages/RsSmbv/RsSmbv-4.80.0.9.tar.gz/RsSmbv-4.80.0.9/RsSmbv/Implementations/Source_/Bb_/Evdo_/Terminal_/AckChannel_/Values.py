from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Values:
	"""Values commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("values", core, parent)

	def set(self, values: List[str], stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:ACKChannel:VALues \n
		(enabled for access terminal working in traffic mode) Specifies the data pattern transmitted on the ACK Channel.
		The sequence starts at frame 0 and slot 0 and is repeated with the length of the pattern.A 0 specifies an ACK, a 1
		specifies a NAK. The pattern is only read for slots that are gated on. This parameter is in binary format and has a
		maximal length of 16 bits. \n
			:param values: integer
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')"""
		param = Conversions.list_to_csv_str(values)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:ACKChannel:VALues {param}')

	def get(self, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:ACKChannel:VALues \n
		(enabled for access terminal working in traffic mode) Specifies the data pattern transmitted on the ACK Channel.
		The sequence starts at frame 0 and slot 0 and is repeated with the length of the pattern.A 0 specifies an ACK, a 1
		specifies a NAK. The pattern is only read for slots that are gated on. This parameter is in binary format and has a
		maximal length of 16 bits. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: values: integer"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:ACKChannel:VALues?')
		return Conversions.str_to_str_list(response)
