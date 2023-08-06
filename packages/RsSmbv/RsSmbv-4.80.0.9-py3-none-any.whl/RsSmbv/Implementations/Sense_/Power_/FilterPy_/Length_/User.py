from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)

	def set(self, user: float, channel=repcap.Channel.Default) -> None:
		"""SENSe<CH>:[POWer]:FILTer:LENGth:[USER] \n
		Selects the filter length for SENS:POW:FILT:'TYPE USER. As the filter length works as a multiplier for the time window, a
		constant filter length results in a constant measurement time (see also 'About the measuring principle, averaging filter,
		filter length, and achieving stable results') .
			INTRO_CMD_HELP: The R&S NRP power sensors provide different resolutions for setting the filter length, depending on the used sensor type: \n
			- Resolution = 1 for R&S NRPxx power sensors
			- Resolution = 2n for sensors of the R&S NRP-Zxx family, with n = 1 to 16 \n
			:param user: float Range: 1 to 65536
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		param = Conversions.decimal_value_to_str(user)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:FILTer:LENGth:USER {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SENSe<CH>:[POWer]:FILTer:LENGth:[USER] \n
		Selects the filter length for SENS:POW:FILT:'TYPE USER. As the filter length works as a multiplier for the time window, a
		constant filter length results in a constant measurement time (see also 'About the measuring principle, averaging filter,
		filter length, and achieving stable results') .
			INTRO_CMD_HELP: The R&S NRP power sensors provide different resolutions for setting the filter length, depending on the used sensor type: \n
			- Resolution = 1 for R&S NRPxx power sensors
			- Resolution = 2n for sensors of the R&S NRP-Zxx family, with n = 1 to 16 \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: user: float Range: 1 to 65536"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:FILTer:LENGth:USER?')
		return Conversions.str_to_float(response)
