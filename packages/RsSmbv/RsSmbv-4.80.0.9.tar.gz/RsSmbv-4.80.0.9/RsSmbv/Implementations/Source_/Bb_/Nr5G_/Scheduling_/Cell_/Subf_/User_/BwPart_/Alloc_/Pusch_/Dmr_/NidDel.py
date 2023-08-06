from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NidDel:
	"""NidDel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nidDel", core, parent)

	def set(self, pusch_dmrs_id_sel: enums.NrsIdAll, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUSCh:DMR:NIDSel \n
		Sets whether the variable nIDCELL or nIDPUSCH is used by the generation of the DMRS sequence. \n
			:param pusch_dmrs_id_sel: CID| PUID CID nIDCELL is used by the generation of the DMRS sequence PUID nIDPUSCH is used by the generation of the DMRS sequence
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(pusch_dmrs_id_sel, enums.NrsIdAll)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUSCh:DMR:NIDSel {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.NrsIdAll:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PUSCh:DMR:NIDSel \n
		Sets whether the variable nIDCELL or nIDPUSCH is used by the generation of the DMRS sequence. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: pusch_dmrs_id_sel: CID| PUID CID nIDCELL is used by the generation of the DMRS sequence PUID nIDPUSCH is used by the generation of the DMRS sequence"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PUSCh:DMR:NIDSel?')
		return Conversions.str_to_scalar_enum(response, enums.NrsIdAll)
