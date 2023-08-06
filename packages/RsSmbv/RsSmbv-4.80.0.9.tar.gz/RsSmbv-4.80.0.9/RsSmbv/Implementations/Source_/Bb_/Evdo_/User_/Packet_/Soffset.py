from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Soffset:
	"""Soffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("soffset", core, parent)

	def set(self, so_ffset: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:PACKet:SOFFset \n
		Sets the minimum number of slots between the end of one packet and the beginning of the next. For single slot packets, a
		value of zero will cause the next packet to be sent in the immediate next slot (subject to scheduling) . For multiple
		slot packets, a value of zero will cause the next packet transmission to start three slots after the end of the previous
		packet. The three slot delay is identical to the interleaving delay between slots for multiple slot packets. The offset
		value is attached to the end of the preceding packet. \n
			:param so_ffset: integer Range: 0 to 255
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.decimal_value_to_str(so_ffset)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:PACKet:SOFFset {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:PACKet:SOFFset \n
		Sets the minimum number of slots between the end of one packet and the beginning of the next. For single slot packets, a
		value of zero will cause the next packet to be sent in the immediate next slot (subject to scheduling) . For multiple
		slot packets, a value of zero will cause the next packet transmission to start three slots after the end of the previous
		packet. The three slot delay is identical to the interleaving delay between slots for multiple slot packets. The offset
		value is attached to the end of the preceding packet. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: so_ffset: integer Range: 0 to 255"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:PACKet:SOFFset?')
		return Conversions.str_to_int(response)
