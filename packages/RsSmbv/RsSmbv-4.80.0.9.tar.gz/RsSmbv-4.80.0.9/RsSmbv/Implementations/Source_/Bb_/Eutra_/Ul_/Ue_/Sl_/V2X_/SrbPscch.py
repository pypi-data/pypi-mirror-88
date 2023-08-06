from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SrbPscch:
	"""SrbPscch commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("srbPscch", core, parent)

	def set(self, start_rb_pscch: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:V2X:SRBPscch \n
		No command help available \n
			:param start_rb_pscch: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.decimal_value_to_str(start_rb_pscch)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:V2X:SRBPscch {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:V2X:SRBPscch \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: start_rb_pscch: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:V2X:SRBPscch?')
		return Conversions.str_to_int(response)
