from ..............Internal.Core import Core
from ..............Internal.CommandsGroup import CommandsGroup
from ..............Internal import Conversions
from .............. import enums
from .............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scid:
	"""Scid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scid", core, parent)

	def set(self, tp_ptrs_scram_id: enums.NrsIdAll, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUSCh:PTRS:TP:SCID \n
		Sets whether the PTRS Scrambling ID value used for the PTRS sequence generation is configured by the 'NPusch ID' (higher
		layer) or by the cell ID. \n
			:param tp_ptrs_scram_id: CID| PUID CID Sets the cell ID as the scrambling ID for PTRS sequence generation. PUID Sets the 'NPusch ID' as the scrambling ID for PTRS sequence generation.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(tp_ptrs_scram_id, enums.NrsIdAll)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUSCh:PTRS:TP:SCID {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.NrsIdAll:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUSCh:PTRS:TP:SCID \n
		Sets whether the PTRS Scrambling ID value used for the PTRS sequence generation is configured by the 'NPusch ID' (higher
		layer) or by the cell ID. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: tp_ptrs_scram_id: CID| PUID CID Sets the cell ID as the scrambling ID for PTRS sequence generation. PUID Sets the 'NPusch ID' as the scrambling ID for PTRS sequence generation."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUSCh:PTRS:TP:SCID?')
		return Conversions.str_to_scalar_enum(response, enums.NrsIdAll)
