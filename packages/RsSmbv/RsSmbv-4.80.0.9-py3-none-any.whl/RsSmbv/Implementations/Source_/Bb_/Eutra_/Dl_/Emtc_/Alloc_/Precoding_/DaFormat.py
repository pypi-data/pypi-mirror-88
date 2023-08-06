from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DaFormat:
	"""DaFormat commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("daFormat", core, parent)

	def set(self, coord_map_mode: enums.CoordMapMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:PRECoding:DAFormat \n
		Switches between the cartesian and cylindrical coordinates representation. \n
			:param coord_map_mode: CARTesian| CYLindrical
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(coord_map_mode, enums.CoordMapMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:PRECoding:DAFormat {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.CoordMapMode:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:PRECoding:DAFormat \n
		Switches between the cartesian and cylindrical coordinates representation. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: coord_map_mode: CARTesian| CYLindrical"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:PRECoding:DAFormat?')
		return Conversions.str_to_scalar_enum(response, enums.CoordMapMode)
