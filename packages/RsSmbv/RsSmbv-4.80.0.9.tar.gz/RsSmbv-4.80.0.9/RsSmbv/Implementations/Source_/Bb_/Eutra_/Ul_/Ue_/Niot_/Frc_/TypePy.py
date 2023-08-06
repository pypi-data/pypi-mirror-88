from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, frc_id: enums.All, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:FRC:TYPE \n
		Selects the FRC. \n
			:param frc_id: A141| A142| A143| A151| A144| A152| A161| A162| A163| A164| A165| A241| A242| A243| A244| A245| A246| A247
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(frc_id, enums.All)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:FRC:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.All:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:FRC:TYPE \n
		Selects the FRC. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: frc_id: A141| A142| A143| A151| A144| A152| A161| A162| A163| A164| A165| A241| A242| A243| A244| A245| A246| A247"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:FRC:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.All)
