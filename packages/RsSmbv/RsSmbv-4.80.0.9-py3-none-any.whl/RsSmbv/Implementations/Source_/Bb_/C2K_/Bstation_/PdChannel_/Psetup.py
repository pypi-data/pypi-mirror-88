from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Psetup:
	"""Psetup commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("psetup", core, parent)

	def set(self, psetup: bool, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:PSETup \n
		Selects for F-PDCH if all subpackets are generated using the same settings or if the settings of subchannel 1 are valid
		for all sub channels. However, the value of 'Number of Bits per Encoder Packet' is a quality of the complete encoder
		packet, therefore it is always set for all sub packet channels via the entry for sub channel 1. \n
			:param psetup: 0| 1| OFF| ON ON Packet parameters can be changed only for sub packet 1, all sub packets are generated with these settings. OFF Packet parameters can be set individually for each sub packet.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.bool_to_str(psetup)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:PSETup {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:PSETup \n
		Selects for F-PDCH if all subpackets are generated using the same settings or if the settings of subchannel 1 are valid
		for all sub channels. However, the value of 'Number of Bits per Encoder Packet' is a quality of the complete encoder
		packet, therefore it is always set for all sub packet channels via the entry for sub channel 1. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: psetup: 0| 1| OFF| ON ON Packet parameters can be changed only for sub packet 1, all sub packets are generated with these settings. OFF Packet parameters can be set individually for each sub packet."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:PSETup?')
		return Conversions.str_to_bool(response)
