from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unscaled:
	"""Unscaled commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("unscaled", core, parent)

	def set(self, a_1: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:TIME:CONVersion:SBAS<ST>:GAGAN:UTC:AONE:UNSCaled \n
		Sets the first order term of polynomial, A1. \n
			:param a_1: integer Range: -8388608 to 8388607
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')"""
		param = Conversions.decimal_value_to_str(a_1)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:SBAS{stream_cmd_val}:GAGAN:UTC:AONE:UNSCaled {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:TIME:CONVersion:SBAS<ST>:GAGAN:UTC:AONE:UNSCaled \n
		Sets the first order term of polynomial, A1. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: a_1: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:SBAS{stream_cmd_val}:GAGAN:UTC:AONE:UNSCaled?')
		return Conversions.str_to_float(response)
