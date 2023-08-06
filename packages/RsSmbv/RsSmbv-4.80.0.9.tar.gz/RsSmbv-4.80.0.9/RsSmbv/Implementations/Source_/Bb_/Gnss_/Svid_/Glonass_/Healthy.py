from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Healthy:
	"""Healthy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("healthy", core, parent)

	def set(self, healthy_state: bool, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass<ST>:HEALthy \n
		Indicates if the selected SV ID is healthy or not. \n
			:param healthy_state: 0| 1| OFF| ON 1 = healthy satellite The healthy state reflects the value of the corresponding healthy flag in the navigation message: method RsSmbv.Source.Bb.Gnss.Svid.Gps.Nmessage.Lnav.Ephemeris.Health.set method RsSmbv.Source.Bb.Gnss.Svid.Gps.Nmessage.Cnav.Ephemeris.L1Health.set method RsSmbv.Source.Bb.Gnss.Svid.Gps.Nmessage.Cnav.Ephemeris.L2Health.set method RsSmbv.Source.Bb.Gnss.Svid.Gps.Nmessage.Cnav.Ephemeris.L5Health.set method RsSmbv.Source.Bb.Gnss.Svid.Galileo.Nmessage.Inav.E1Bdvs.set method RsSmbv.Source.Bb.Gnss.Svid.Galileo.Nmessage.Inav.E1Bhs.set method RsSmbv.Source.Bb.Gnss.Svid.Galileo.Nmessage.Inav.E5Bhs.set method RsSmbv.Source.Bb.Gnss.Svid.Beidou.Nmessage.Dnav.Ephemeris.Health.set method RsSmbv.Source.Bb.Gnss.Svid.Glonass.Nmessage.Nav.Ephemeris.Health.set method RsSmbv.Source.Bb.Gnss.Svid.Qzss.Nmessage.Nav.Ephemeris.Health.set The values are interdependent; changing one of them changes the other.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')"""
		param = Conversions.bool_to_str(healthy_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GLONass{stream_cmd_val}:HEALthy {param}')

	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GLONass<ST>:HEALthy \n
		Indicates if the selected SV ID is healthy or not. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Glonass')
			:return: healthy_state: 0| 1| OFF| ON 1 = healthy satellite The healthy state reflects the value of the corresponding healthy flag in the navigation message: method RsSmbv.Source.Bb.Gnss.Svid.Gps.Nmessage.Lnav.Ephemeris.Health.set method RsSmbv.Source.Bb.Gnss.Svid.Gps.Nmessage.Cnav.Ephemeris.L1Health.set method RsSmbv.Source.Bb.Gnss.Svid.Gps.Nmessage.Cnav.Ephemeris.L2Health.set method RsSmbv.Source.Bb.Gnss.Svid.Gps.Nmessage.Cnav.Ephemeris.L5Health.set method RsSmbv.Source.Bb.Gnss.Svid.Galileo.Nmessage.Inav.E1Bdvs.set method RsSmbv.Source.Bb.Gnss.Svid.Galileo.Nmessage.Inav.E1Bhs.set method RsSmbv.Source.Bb.Gnss.Svid.Galileo.Nmessage.Inav.E5Bhs.set method RsSmbv.Source.Bb.Gnss.Svid.Beidou.Nmessage.Dnav.Ephemeris.Health.set method RsSmbv.Source.Bb.Gnss.Svid.Glonass.Nmessage.Nav.Ephemeris.Health.set method RsSmbv.Source.Bb.Gnss.Svid.Qzss.Nmessage.Nav.Ephemeris.Health.set The values are interdependent; changing one of them changes the other."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GLONass{stream_cmd_val}:HEALthy?')
		return Conversions.str_to_bool(response)
