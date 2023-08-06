from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sformat:
	"""Sformat commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sformat", core, parent)

	def set(self, sf_ormat: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:SFORmat \n
		Defines the slot format of the PRACH. A change of slot format leads to an automatic change of symbol rate method RsSmbv.
		Source.Bb.W3Gpp.Mstation.Prach.SymbolRate.set When channel coding is active, the slot format is predetermined. So in this
		case, the command has no effect. \n
			:param sf_ormat: 0 | 1 | 2 | 3
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(sf_ormat)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PRACh:SFORmat {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:SFORmat \n
		Defines the slot format of the PRACH. A change of slot format leads to an automatic change of symbol rate method RsSmbv.
		Source.Bb.W3Gpp.Mstation.Prach.SymbolRate.set When channel coding is active, the slot format is predetermined. So in this
		case, the command has no effect. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: sf_ormat: 0 | 1 | 2 | 3"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PRACh:SFORmat?')
		return Conversions.str_to_int(response)
