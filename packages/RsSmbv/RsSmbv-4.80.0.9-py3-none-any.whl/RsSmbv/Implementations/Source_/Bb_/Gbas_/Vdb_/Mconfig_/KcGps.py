from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class KcGps:
	"""KcGps commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("kcGps", core, parent)

	def set(self, kmd_ec_gps: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:KCGPs \n
		Sets the ephemeris missed detection parameter (Kmd_e) , category I precision approach and approach with vertical guidance
		(APV) . This is a multiplier considered when calculating the ephemeris error position bound for the category I precision
		approach and APV. It is derived from the probability that a detection is missed because of an ephemeris error in a
		GPS/GLONASS satellite. \n
			:param kmd_ec_gps: float Range: 0 to 12.75
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.decimal_value_to_str(kmd_ec_gps)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:KCGPs {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:KCGPs \n
		Sets the ephemeris missed detection parameter (Kmd_e) , category I precision approach and approach with vertical guidance
		(APV) . This is a multiplier considered when calculating the ephemeris error position bound for the category I precision
		approach and APV. It is derived from the probability that a detection is missed because of an ephemeris error in a
		GPS/GLONASS satellite. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: kmd_ec_gps: float Range: 0 to 12.75"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:KCGPs?')
		return Conversions.str_to_float(response)
