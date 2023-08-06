from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class KpGlonass:
	"""KpGlonass commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("kpGlonass", core, parent)

	def set(self, kmd_epos_glonass: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:KPGLonass \n
		Sets the ephemeris missed detection parameter (Kmd_e) , GBAS positioning service . This is a multiplier considered when
		calculating the ephemeris error position bound for the GBAS positioning. It is derived from the probability that a
		detection is missed because of an ephemeris error in a GPS/GLONASS satellite. \n
			:param kmd_epos_glonass: float Range: 0 to 12.75
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.decimal_value_to_str(kmd_epos_glonass)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:KPGLonass {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:KPGLonass \n
		Sets the ephemeris missed detection parameter (Kmd_e) , GBAS positioning service . This is a multiplier considered when
		calculating the ephemeris error position bound for the GBAS positioning. It is derived from the probability that a
		detection is missed because of an ephemeris error in a GPS/GLONASS satellite. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: kmd_epos_glonass: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:KPGLonass?')
		return Conversions.str_to_float(response)
