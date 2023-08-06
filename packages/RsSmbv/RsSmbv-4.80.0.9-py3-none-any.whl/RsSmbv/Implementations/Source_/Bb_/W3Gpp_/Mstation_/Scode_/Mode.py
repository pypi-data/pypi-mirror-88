from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.ScrCodeMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:SCODe:MODE \n
		The command sets the type for the scrambling code. The scrambling code generator can also be deactivated for test
		purposes. SHORt is only standardized for the selection BB:W3GP:MST:MODE DPCDh and BB:W3GP:MST:MODE PCPCh. But it can also
		be generated for the PCPCH for test purposes. \n
			:param mode: LONG| SHORt| OFF
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(mode, enums.ScrCodeMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:SCODe:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.ScrCodeMode:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:SCODe:MODE \n
		The command sets the type for the scrambling code. The scrambling code generator can also be deactivated for test
		purposes. SHORt is only standardized for the selection BB:W3GP:MST:MODE DPCDh and BB:W3GP:MST:MODE PCPCh. But it can also
		be generated for the PCPCH for test purposes. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: mode: LONG| SHORt| OFF"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:SCODe:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ScrCodeMode)
