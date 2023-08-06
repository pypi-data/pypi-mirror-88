from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Period:
	"""Period commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("period", core, parent)

	def set(self, utc_offset_period: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SYSTem:SBAS:EGNOS<ST>:NMESsage:NAV:UTCoffset:PERiod \n
		Sets the periodicity of the SBAS message. \n
			:param utc_offset_period: integer Range: 0 to 999
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')"""
		param = Conversions.decimal_value_to_str(utc_offset_period)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SYSTem:SBAS:EGNOS{stream_cmd_val}:NMESsage:NAV:UTCoffset:PERiod {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:SYSTem:SBAS:EGNOS<ST>:NMESsage:NAV:UTCoffset:PERiod \n
		Sets the periodicity of the SBAS message. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')
			:return: utc_offset_period: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SYSTem:SBAS:EGNOS{stream_cmd_val}:NMESsage:NAV:UTCoffset:PERiod?')
		return Conversions.str_to_int(response)
