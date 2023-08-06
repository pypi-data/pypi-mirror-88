from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OltDiversity:
	"""OltDiversity commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("oltDiversity", core, parent)

	def set(self, olt_diversity: bool, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:OLTDiversity \n
		Activates/deactivates open loop transmit diversity. The antenna whose signal is to be simulated is selected with the
		command method RsSmbv.Source.Bb.W3Gpp.Bstation.Tdiversity.set. \n
			:param olt_diversity: ON| OFF
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.bool_to_str(olt_diversity)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:OLTDiversity {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:OLTDiversity \n
		Activates/deactivates open loop transmit diversity. The antenna whose signal is to be simulated is selected with the
		command method RsSmbv.Source.Bb.W3Gpp.Bstation.Tdiversity.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: olt_diversity: ON| OFF"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:OLTDiversity?')
		return Conversions.str_to_bool(response)
