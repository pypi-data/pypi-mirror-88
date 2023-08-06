from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	def set(self, srate: enums.SymbRate, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:SRATe \n
		The command sets the symbol rate of the PCPCH. User Equipment 1: When channel coding is active, the symbol rate is
		limited to the range between 15 and 120 ksps. Values above this limit are automatically set to 120 ksps. \n
			:param srate: D15K| D30K| D60K| D120k| D240k| D480k| D960k
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(srate, enums.SymbRate)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:SRATe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.SymbRate:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:SRATe \n
		The command sets the symbol rate of the PCPCH. User Equipment 1: When channel coding is active, the symbol rate is
		limited to the range between 15 and 120 ksps. Values above this limit are automatically set to 120 ksps. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: srate: D15K| D30K| D60K| D120k| D240k| D480k| D960k"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:SRATe?')
		return Conversions.str_to_scalar_enum(response, enums.SymbRate)
