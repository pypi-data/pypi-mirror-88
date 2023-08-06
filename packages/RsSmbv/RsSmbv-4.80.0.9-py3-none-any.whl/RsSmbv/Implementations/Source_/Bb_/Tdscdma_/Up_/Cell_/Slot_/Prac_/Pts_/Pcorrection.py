from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pcorrection:
	"""Pcorrection commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pcorrection", core, parent)

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:TDSCdma:UP:CELL<ST>:SLOT<CH>:PRAC:PTS:PCORrection \n
		Queries the power correction of the UpPTS.
			INTRO_CMD_HELP: The value is computed based on: \n
			- UpPTS power method RsSmbv.Source.Bb.Tdscdma.Up.Cell.Slot.Prac.Pts.Power.set
			- Power step method RsSmbv.Source.Bb.Tdscdma.Up.Cell.Slot.Prac.Pts.Pstep.set
			- Message power method RsSmbv.Source.Bb.Tdscdma.Up.Cell.Slot.Prac.Msg.Power.set
			- UpPTS length, message length method RsSmbv.Source.Bb.Tdscdma.Up.Cell.Slot.Prac.Msg.Length.set
			- ARB sequence length method RsSmbv.Source.Bb.Tdscdma.slength \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slot')
			:return: pcorrection: float Range: -1E10 to 1E10"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:UP:CELL{stream_cmd_val}:SLOT{channel_cmd_val}:PRAC:PTS:PCORrection?')
		return Conversions.str_to_float(response)
