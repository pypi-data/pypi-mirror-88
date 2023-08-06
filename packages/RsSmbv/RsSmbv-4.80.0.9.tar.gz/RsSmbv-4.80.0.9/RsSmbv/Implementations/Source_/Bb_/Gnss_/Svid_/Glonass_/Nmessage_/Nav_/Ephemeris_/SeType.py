from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SeType:
	"""SeType commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("seType", core, parent)

	def set(self, sat_type: enums.EphSatType, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass<ST>:NMESsage:NAV:EPHemeris:SEType \n
		Sets the satellite ephemeris type - M parameter. \n
			:param sat_type: GLO| GLOM
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')"""
		param = Conversions.enum_scalar_to_str(sat_type, enums.EphSatType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GLONass{stream_cmd_val}:NMESsage:NAV:EPHemeris:SEType {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.EphSatType:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass<ST>:NMESsage:NAV:EPHemeris:SEType \n
		Sets the satellite ephemeris type - M parameter. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:return: sat_type: GLO| GLOM"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GLONass{stream_cmd_val}:NMESsage:NAV:EPHemeris:SEType?')
		return Conversions.str_to_scalar_enum(response, enums.EphSatType)
