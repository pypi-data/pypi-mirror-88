from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MapCoordinates:
	"""MapCoordinates commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mapCoordinates", core, parent)

	def set(self, map_coord: enums.CoordMapMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:APM:MAPCoordinates \n
		Switches between the Cartesian (Real/Imag.) and Cylindrical (Magn./Phase) coordinates representation. \n
			:param map_coord: CARTesian| CYLindrical
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(map_coord, enums.CoordMapMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:APM:MAPCoordinates {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.CoordMapMode:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:APM:MAPCoordinates \n
		Switches between the Cartesian (Real/Imag.) and Cylindrical (Magn./Phase) coordinates representation. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: map_coord: CARTesian| CYLindrical"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:APM:MAPCoordinates?')
		return Conversions.str_to_scalar_enum(response, enums.CoordMapMode)
