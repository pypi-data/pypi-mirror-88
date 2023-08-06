from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CpsFormat:
	"""CpsFormat commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cpsFormat", core, parent)

	def set(self, cps_format: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:CPSFormat \n
		The command defines the slot format of the control component of the PCPCH.
			INTRO_CMD_HELP: The slot format sets the associated FBI mode automatically: \n
			- Slot format 0 = FBI OFF
			- Slot format 1 = FBI 1 bit
			- Slot format 2 = FBI 2 bits \n
			:param cps_format: integer Range: 0 to 2
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(cps_format)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:CPSFormat {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:CPSFormat \n
		The command defines the slot format of the control component of the PCPCH.
			INTRO_CMD_HELP: The slot format sets the associated FBI mode automatically: \n
			- Slot format 0 = FBI OFF
			- Slot format 1 = FBI 1 bit
			- Slot format 2 = FBI 2 bits \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: cps_format: integer Range: 0 to 2"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:CPSFormat?')
		return Conversions.str_to_int(response)
