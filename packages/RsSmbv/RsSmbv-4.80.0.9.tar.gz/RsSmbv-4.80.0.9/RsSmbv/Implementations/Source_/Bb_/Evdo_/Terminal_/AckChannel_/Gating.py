from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gating:
	"""Gating commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gating", core, parent)

	def set(self, gating: List[str], stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:ACKChannel:GATing \n
		(enabled for access terminal working in traffic mode) Sets the active and inactive slots of the ACK channel.
		This parameter is in binary format and has a maximal length of 16 bits. The sequence starts at frame 0 and slot 0 and is
		repeated with the length of the pattern. A 0 gates the ACK channel off for the corresponding slot, a 1 activates the
		channel. \n
			:param gating: integer
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')"""
		param = Conversions.list_to_csv_str(gating)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:ACKChannel:GATing {param}')

	def get(self, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:ACKChannel:GATing \n
		(enabled for access terminal working in traffic mode) Sets the active and inactive slots of the ACK channel.
		This parameter is in binary format and has a maximal length of 16 bits. The sequence starts at frame 0 and slot 0 and is
		repeated with the length of the pattern. A 0 gates the ACK channel off for the corresponding slot, a 1 activates the
		channel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: gating: integer"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:ACKChannel:GATing?')
		return Conversions.str_to_str_list(response)
