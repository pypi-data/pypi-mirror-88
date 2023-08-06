from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Duration:
	"""Duration commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("duration", core, parent)

	def set(self, duration: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:BEIDou<ST>:TOAData:DURation \n
		Sets the duration of the assistance data. \n
			:param duration: float Range: 1E-3 to 5E3
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')"""
		param = Conversions.decimal_value_to_str(duration)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:BEIDou{stream_cmd_val}:TOAData:DURation {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:BEIDou<ST>:TOAData:DURation \n
		Sets the duration of the assistance data. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Beidou')
			:return: duration: float Range: 1E-3 to 5E3"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:BEIDou{stream_cmd_val}:TOAData:DURation?')
		return Conversions.str_to_float(response)
