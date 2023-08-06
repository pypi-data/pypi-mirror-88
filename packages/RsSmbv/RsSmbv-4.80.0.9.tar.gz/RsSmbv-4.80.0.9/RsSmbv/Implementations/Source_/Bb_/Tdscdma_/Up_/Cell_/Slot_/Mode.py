from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.TdscdmaSlotModeUp, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH>:MODE \n
		Sets the mode in which the slot is to work. \n
			:param mode: DEDicated| PRACh DEDicated The instrument generates a signal with a dedicated physical control channel (DPCCH) and up to six dedicated physical data channels (DPDCH) . The signal is used for voice and data transmission. PRACh The instrument generates a single physical random access channel (PRACH) . This channel is needed to set up the connection between the mobile station and the base station.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')"""
		param = Conversions.enum_scalar_to_str(mode, enums.TdscdmaSlotModeUp)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.TdscdmaSlotModeUp:
		"""[SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH>:MODE \n
		Sets the mode in which the slot is to work. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:return: mode: DEDicated| PRACh DEDicated The instrument generates a signal with a dedicated physical control channel (DPCCH) and up to six dedicated physical data channels (DPDCH) . The signal is used for voice and data transmission. PRACh The instrument generates a single physical random access channel (PRACH) . This channel is needed to set up the connection between the mobile station and the base station."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.TdscdmaSlotModeUp)
