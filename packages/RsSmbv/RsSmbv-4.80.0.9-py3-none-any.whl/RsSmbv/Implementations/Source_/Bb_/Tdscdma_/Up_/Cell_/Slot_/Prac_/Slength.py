from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slength:
	"""Slength commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slength", core, parent)

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH>:PRAC:SLENgth \n
		Queries the sequence length of the PRACH slot.
			INTRO_CMD_HELP: The value is computed based on: \n
			- Start Subframe method RsSmbv.Source.Bb.Tdscdma.Up.Cell.Slot.Prac.Pts.Start.set
			- UpPTS repetition method RsSmbv.Source.Bb.Tdscdma.Up.Cell.Slot.Prac.Pts.Repetition.set
			- Distance UpPTS and RACH method RsSmbv.Source.Bb.Tdscdma.Up.Cell.Slot.Prac.Pts.Distance.set
			- Message length method RsSmbv.Source.Bb.Tdscdma.Up.Cell.Slot.Prac.Msg.Length.set \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:return: slength: float Range: 0.5 to 13.5"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:PRAC:SLENgth?')
		return Conversions.str_to_float(response)
