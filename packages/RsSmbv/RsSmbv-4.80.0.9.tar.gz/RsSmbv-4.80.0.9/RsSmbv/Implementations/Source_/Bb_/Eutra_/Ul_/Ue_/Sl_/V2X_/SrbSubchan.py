from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SrbSubchan:
	"""SrbSubchan commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("srbSubchan", core, parent)

	def set(self, start_rb_subchan: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:V2X:SRBSubchan \n
		Sets the first RB in the subchannel. \n
			:param start_rb_subchan: integer Range: 0 to 99
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.decimal_value_to_str(start_rb_subchan)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:V2X:SRBSubchan {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:V2X:SRBSubchan \n
		Sets the first RB in the subchannel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: start_rb_subchan: integer Range: 0 to 99"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:V2X:SRBSubchan?')
		return Conversions.str_to_int(response)
