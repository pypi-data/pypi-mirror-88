from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class System:
	"""System commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("system", core, parent)

	def set(self, system: enums.Hybrid, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:TRAJectory:SYSTem \n
		Selects the GNSS system which elevation/azimuth variation over 24 hours is displayed. \n
			:param system: GPS| GALileo| GLONass| BEIDou| QZSS| SBAS
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')"""
		param = Conversions.enum_scalar_to_str(system, enums.Hybrid)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay:TRAJectory:SYSTem {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.Hybrid:
		"""[SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:TRAJectory:SYSTem \n
		Selects the GNSS system which elevation/azimuth variation over 24 hours is displayed. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')
			:return: system: GPS| GALileo| GLONass| BEIDou| QZSS| SBAS"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay:TRAJectory:SYSTem?')
		return Conversions.str_to_scalar_enum(response, enums.Hybrid)
