from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal.Utilities import trim_str_response
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SltSymbols:
	"""SltSymbols commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sltSymbols", core, parent)

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> str:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUSCh:DMRS:SLTSymbols \n
		Queries the slot number of DMRS symbols. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: pxsch_dmrs_slot_sy: string Range: 0 char to 256 char"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUSCh:DMRS:SLTSymbols?')
		return trim_str_response(response)
