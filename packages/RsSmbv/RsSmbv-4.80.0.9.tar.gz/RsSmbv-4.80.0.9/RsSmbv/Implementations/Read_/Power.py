from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def get(self, channel=repcap.Channel.Default) -> List[float]:
		"""READ<CH>:[POWer] \n
		Triggers power measurement and displays the results. Note: This command does not affect the local state, i.e. you can get
		results with local state on or off. For long measurement times, we recommend that you use an SRQ for command
		synchronization (MAV bit) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Read')
			:return: power: float or float,float The sensor returns the result in the unit set with command SENSech Certain power sensors, such as the R&S NRP-Z81, return two values, first the value of the average level and - separated by a comma - the peak value."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_bin_or_ascii_float_list(f'READ{channel_cmd_val}:POWer?')
		return response
