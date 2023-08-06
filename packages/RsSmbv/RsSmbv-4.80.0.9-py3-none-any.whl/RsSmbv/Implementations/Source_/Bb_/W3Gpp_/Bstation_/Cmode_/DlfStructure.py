from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DlfStructure:
	"""DlfStructure commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dlfStructure", core, parent)

	def set(self, dlf_structure: enums.MappingType, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CMODe:DLFStructure \n
		The command selects the frame structure. The frame structure determines the transmission of TPC and pilot field in the
		transmission gaps. \n
			:param dlf_structure: A| B A Type A, the pilot field is sent in the last slot of each transmission gap. B Type B, the pilot field is sent in the last slot of each transmission gap. The first TPC field of the transmission gap is sent in addition.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.enum_scalar_to_str(dlf_structure, enums.MappingType)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CMODe:DLFStructure {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.MappingType:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CMODe:DLFStructure \n
		The command selects the frame structure. The frame structure determines the transmission of TPC and pilot field in the
		transmission gaps. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: dlf_structure: A| B A Type A, the pilot field is sent in the last slot of each transmission gap. B Type B, the pilot field is sent in the last slot of each transmission gap. The first TPC field of the transmission gap is sent in addition."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CMODe:DLFStructure?')
		return Conversions.str_to_scalar_enum(response, enums.MappingType)
