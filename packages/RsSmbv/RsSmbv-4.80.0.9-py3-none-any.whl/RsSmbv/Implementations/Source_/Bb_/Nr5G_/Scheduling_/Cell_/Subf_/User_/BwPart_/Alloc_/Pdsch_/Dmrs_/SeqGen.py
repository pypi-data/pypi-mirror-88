from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeqGen:
	"""SeqGen commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("seqGen", core, parent)

	def set(self, seq_gen: enums.AllPxschSequenceGeneration, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PDSCh:DMRS:SEQGen \n
		Sets how the scrambling ID for DMRS is derived. \n
			:param seq_gen: CELLid| DMRSid DMRSid NIDDMRS: Scrambling ID (i.e. nID) = DMRS scrambling ID (i.e. NIDDMRS) CELLid NIDCell: Scrambling ID (i.e. nID) = cell ID (i.e. NIDCell)
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(seq_gen, enums.AllPxschSequenceGeneration)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PDSCh:DMRS:SEQGen {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.AllPxschSequenceGeneration:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:PDSCh:DMRS:SEQGen \n
		Sets how the scrambling ID for DMRS is derived. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: seq_gen: CELLid| DMRSid DMRSid NIDDMRS: Scrambling ID (i.e. nID) = DMRS scrambling ID (i.e. NIDDMRS) CELLid NIDCell: Scrambling ID (i.e. nID) = cell ID (i.e. NIDCell)"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:PDSCh:DMRS:SEQGen?')
		return Conversions.str_to_scalar_enum(response, enums.AllPxschSequenceGeneration)
