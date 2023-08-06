from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Select:
	"""Select commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("select", core, parent)

	def set(self, location: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:[SELect] \n
		Selects the geographic location of the GNSS receiver. \n
			:param location: 'User Defined' | 'New York' | 'San Francisco' | 'Beijing' | 'New Delhi' | 'Seoul' | 'Singapore' | 'Taipei' | 'Tokyo' | 'Sydney' | 'London' | 'Moscow' | 'Munich' | 'Paris' User Defined Enables the definition of the 'Latitude', 'Longitude' and 'Altitude' of the GNSS receiver with fixed position in the ECEF WGS84 coordinate system. 'New York' | 'San Francisco' | 'Beijing' | 'New Delhi' | 'Seoul' | 'Singapore' | 'Taipei' | 'Tokyo' | 'Sydney' | 'London' | 'Moscow' | 'Munich' | 'Paris' Selects one of the predefined fixed geographic locations. The parameters latitude, longitude and altitude are set according to the selected position.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.value_to_quoted_str(location)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:LOCation:SELect {param}')

	def get(self, stream=repcap.Stream.Default) -> str:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:[SELect] \n
		Selects the geographic location of the GNSS receiver. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: location: 'User Defined' | 'New York' | 'San Francisco' | 'Beijing' | 'New Delhi' | 'Seoul' | 'Singapore' | 'Taipei' | 'Tokyo' | 'Sydney' | 'London' | 'Moscow' | 'Munich' | 'Paris' User Defined Enables the definition of the 'Latitude', 'Longitude' and 'Altitude' of the GNSS receiver with fixed position in the ECEF WGS84 coordinate system. 'New York' | 'San Francisco' | 'Beijing' | 'New Delhi' | 'Seoul' | 'Singapore' | 'Taipei' | 'Tokyo' | 'Sydney' | 'London' | 'Moscow' | 'Munich' | 'Paris' Selects one of the predefined fixed geographic locations. The parameters latitude, longitude and altitude are set according to the selected position."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:LOCation:SELect?')
		return trim_str_response(response)
