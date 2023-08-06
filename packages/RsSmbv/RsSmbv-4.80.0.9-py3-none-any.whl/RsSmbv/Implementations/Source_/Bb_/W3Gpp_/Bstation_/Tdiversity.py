from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tdiversity:
	"""Tdiversity commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tdiversity", core, parent)

	def set(self, tdiversity: enums.TxDiv, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:TDIVersity \n
		Selects the antenna and the antenna configuration to be simulated. To simulate transmit diversity, a two-antenna system
		has to be selected and Open Loop Transmit Diversity has to be activated (command BB:W3GP:BST:OLTD ON) . \n
			:param tdiversity: SANT| ANT1| ANT2| OFF SANT = single-antenna system
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.enum_scalar_to_str(tdiversity, enums.TxDiv)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:TDIVersity {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.TxDiv:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:TDIVersity \n
		Selects the antenna and the antenna configuration to be simulated. To simulate transmit diversity, a two-antenna system
		has to be selected and Open Loop Transmit Diversity has to be activated (command BB:W3GP:BST:OLTD ON) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: tdiversity: SANT| ANT1| ANT2| OFF SANT = single-antenna system"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:TDIVersity?')
		return Conversions.str_to_scalar_enum(response, enums.TxDiv)
