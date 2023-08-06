from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NnPrep:
	"""NnPrep commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nnPrep", core, parent)

	def set(self, no_npusch_rep: enums.EutraUlNoNpuschrEpNbIoTaLl, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:FRC:NNPRep \n
		Queries the number of NPUSCH repetitions. \n
			:param no_npusch_rep: 1| 2| 16| 64
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(no_npusch_rep, enums.EutraUlNoNpuschrEpNbIoTaLl)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:FRC:NNPRep {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraUlNoNpuschrEpNbIoTaLl:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:FRC:NNPRep \n
		Queries the number of NPUSCH repetitions. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: no_npusch_rep: 1| 2| 16| 64"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:FRC:NNPRep?')
		return Conversions.str_to_scalar_enum(response, enums.EutraUlNoNpuschrEpNbIoTaLl)
