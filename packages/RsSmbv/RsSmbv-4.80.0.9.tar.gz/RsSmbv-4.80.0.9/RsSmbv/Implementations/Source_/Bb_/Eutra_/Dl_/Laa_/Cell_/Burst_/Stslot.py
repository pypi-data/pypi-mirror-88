from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Stslot:
	"""Stslot commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stslot", core, parent)

	def set(self, starting_slots: enums.EutraLaaStartingSlots, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:LAA:CELL<CH>:BURSt<ST>:STSLot \n
		Sets the starting slot. \n
			:param starting_slots: FIRSt| SECond FIRSt s0: first slot of a subframe SECond s7: second slot of a subframe
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Burst')"""
		param = Conversions.enum_scalar_to_str(starting_slots, enums.EutraLaaStartingSlots)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:LAA:CELL{channel_cmd_val}:BURSt{stream_cmd_val}:STSLot {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.EutraLaaStartingSlots:
		"""[SOURce<HW>]:BB:EUTRa:DL:LAA:CELL<CH>:BURSt<ST>:STSLot \n
		Sets the starting slot. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Burst')
			:return: starting_slots: FIRSt| SECond FIRSt s0: first slot of a subframe SECond s7: second slot of a subframe"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:LAA:CELL{channel_cmd_val}:BURSt{stream_cmd_val}:STSLot?')
		return Conversions.str_to_scalar_enum(response, enums.EutraLaaStartingSlots)
