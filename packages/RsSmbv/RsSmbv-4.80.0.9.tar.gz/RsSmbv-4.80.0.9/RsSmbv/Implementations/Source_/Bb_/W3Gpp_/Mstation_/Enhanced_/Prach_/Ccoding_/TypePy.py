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

	def set(self, type_py: enums.ChanCodTypeEnhPrac, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:ENHanced:PRACh:CCODing:TYPE \n
		The command selects the channel coding scheme in accordance with the 3GPP specification. \n
			:param type_py: TB168| TB360| TU168| TU360 TB168 RACH RMC (TB size 168 bits) TB360 RACH RMC (TB size 360 bits)
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(type_py, enums.ChanCodTypeEnhPrac)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:ENHanced:PRACh:CCODing:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.ChanCodTypeEnhPrac:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:ENHanced:PRACh:CCODing:TYPE \n
		The command selects the channel coding scheme in accordance with the 3GPP specification. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: type_py: TB168| TB360| TU168| TU360 TB168 RACH RMC (TB size 168 bits) TB360 RACH RMC (TB size 360 bits)"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:ENHanced:PRACh:CCODing:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.ChanCodTypeEnhPrac)
