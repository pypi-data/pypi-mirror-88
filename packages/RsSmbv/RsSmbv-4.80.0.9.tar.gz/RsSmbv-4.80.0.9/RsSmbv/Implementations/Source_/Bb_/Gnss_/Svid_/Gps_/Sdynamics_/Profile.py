from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Profile:
	"""Profile commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("profile", core, parent)

	def set(self, profile: enums.Doppler, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:SDYNamics:PROFile \n
		Selects the dynamics profile type. \n
			:param profile: CONStant| HIGH CONStant Constant velocity as set with the command method RsSmbv.Source.Bb.Gnss.Svid.Gps.Sdynamics.Velocity.set. HIGH Profiles with higher-order dynamics as set with the command method RsSmbv.Source.Bb.Gnss.Svid.Gps.Sdynamics.Config.set.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')"""
		param = Conversions.enum_scalar_to_str(profile, enums.Doppler)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:SDYNamics:PROFile {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.Doppler:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:GPS<ST>:SDYNamics:PROFile \n
		Selects the dynamics profile type. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gps')
			:return: profile: CONStant| HIGH CONStant Constant velocity as set with the command method RsSmbv.Source.Bb.Gnss.Svid.Gps.Sdynamics.Velocity.set. HIGH Profiles with higher-order dynamics as set with the command method RsSmbv.Source.Bb.Gnss.Svid.Gps.Sdynamics.Config.set."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:GPS{stream_cmd_val}:SDYNamics:PROFile?')
		return Conversions.str_to_scalar_enum(response, enums.Doppler)
