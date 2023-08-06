from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fcio:
	"""Fcio commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fcio", core, parent)

	def set(self, fcio: bool, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPDCh:E:FCIO \n
		The command sets the channelization code to I/0. \n
			:param fcio: ON| OFF
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.bool_to_str(fcio)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPDCh:E:FCIO {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPDCh:E:FCIO \n
		The command sets the channelization code to I/0. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: fcio: ON| OFF"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPDCh:E:FCIO?')
		return Conversions.str_to_bool(response)
