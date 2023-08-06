from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Aoep:
	"""Aoep commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aoep", core, parent)

	def set(self, age_of_ephemeris: enums.EphAge, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass<ST>:NMESsage:NAV:EPHemeris:AOEP \n
		Sets the age of ephemeris page - P1 parameter. \n
			:param age_of_ephemeris: A30M| A45M| A60M
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')"""
		param = Conversions.enum_scalar_to_str(age_of_ephemeris, enums.EphAge)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GLONass{stream_cmd_val}:NMESsage:NAV:EPHemeris:AOEP {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.EphAge:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass<ST>:NMESsage:NAV:EPHemeris:AOEP \n
		Sets the age of ephemeris page - P1 parameter. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:return: age_of_ephemeris: A30M| A45M| A60M"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GLONass{stream_cmd_val}:NMESsage:NAV:EPHemeris:AOEP?')
		return Conversions.str_to_scalar_enum(response, enums.EphAge)
