from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rvelocity:
	"""Rvelocity commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rvelocity", core, parent)

	def get(self, time_basis: enums.TimeBasis, year: int, month: int, day: int, hour: int, minutes: int, seconds: float, week_number: int, time_of_week: float, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:RT:RECeiver:[V<ST>]:RVELocity \n
		Queries the velocity of the receiver location for the selected moment of time. The required query parameters depend on
		the selected timebase. \n
			:param time_basis: select
			:param year: integer Range: 1980 to 9999
			:param month: integer Range: 1 to 12
			:param day: integer Range: 1 to 31
			:param hour: integer Range: 0 to 23
			:param minutes: integer Range: 0 to 59
			:param seconds: float Range: 0 to 59.999
			:param week_number: integer Range: 0 to 529947
			:param time_of_week: float Range: 0 to 604799.999
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: velocity: float Range: 0 to 1000"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('time_basis', time_basis, DataType.Enum), ArgSingle('year', year, DataType.Integer), ArgSingle('month', month, DataType.Integer), ArgSingle('day', day, DataType.Integer), ArgSingle('hour', hour, DataType.Integer), ArgSingle('minutes', minutes, DataType.Integer), ArgSingle('seconds', seconds, DataType.Float), ArgSingle('week_number', week_number, DataType.Integer), ArgSingle('time_of_week', time_of_week, DataType.Float))
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RT:RECeiver:V{stream_cmd_val}:RVELocity? {param}'.rstrip())
		return Conversions.str_to_float(response)
