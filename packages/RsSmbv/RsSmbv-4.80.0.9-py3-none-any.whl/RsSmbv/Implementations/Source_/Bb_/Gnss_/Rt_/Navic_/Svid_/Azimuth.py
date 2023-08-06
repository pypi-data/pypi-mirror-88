from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Azimuth:
	"""Azimuth commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("azimuth", core, parent)

	def get(self, time_basis: enums.TimeBasis, year: int, month: int, day: int, hour: int, minutes: int, seconds: float, week_number: int, time_of_week: float, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:RT:NAVic<ST>:SVID<CH>:AZIMuth \n
		Queries the satellite azimuth in the selected moment of time. The required query parameters, depend on the selected
		timebase. \n
			:param time_basis: UTC | GPS | GST | GLO | BDT
			:param year: integer Required for TimeBasis = UTC Range: 1980 to 9999
			:param month: integer Required for TimeBasis = UTC Range: 1 to 12
			:param day: integer Required for TimeBasis = UTC Range: 1 to 31
			:param hour: integer Required for TimeBasis = UTC Range: 0 to 23
			:param minutes: integer Required for TimeBasis = UTC Range: 0 to 59
			:param seconds: float Required for TimeBasis = UTC Range: 0 to 59.999
			:param week_number: integer Required for TimeBasis = GPS|GST|BDT Range: 0 to 529947
			:param time_of_week: float Required for TimeBasis = GPS|GST|BDT Range: 0 to 604799.999
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:return: azimuth: float"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('time_basis', time_basis, DataType.Enum), ArgSingle('year', year, DataType.Integer), ArgSingle('month', month, DataType.Integer), ArgSingle('day', day, DataType.Integer), ArgSingle('hour', hour, DataType.Integer), ArgSingle('minutes', minutes, DataType.Integer), ArgSingle('seconds', seconds, DataType.Float), ArgSingle('week_number', week_number, DataType.Integer), ArgSingle('time_of_week', time_of_week, DataType.Float))
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RT:NAVic{stream_cmd_val}:SVID{channel_cmd_val}:AZIMuth? {param}'.rstrip())
		return Conversions.str_to_float(response)
