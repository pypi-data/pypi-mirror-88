from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gate:
	"""Gate commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gate", core, parent)

	def get_edelay(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:GATE:EDELay \n
		Sets the expected reply delay. The expected reply delay and the gate length determine the measurement window (expected
		reply delay +/- gate length/2) . \n
			:return: edelay: float Range: 0 to 150E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:GATE:EDELay?')
		return Conversions.str_to_float(response)

	def set_edelay(self, edelay: float) -> None:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:GATE:EDELay \n
		Sets the expected reply delay. The expected reply delay and the gate length determine the measurement window (expected
		reply delay +/- gate length/2) . \n
			:param edelay: float Range: 0 to 150E-6
		"""
		param = Conversions.decimal_value_to_str(edelay)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ANALysis:GATE:EDELay {param}')

	def get_time(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:GATE:TIME \n
		Sets the DME analysis measurement time. \n
			:return: measurement_time: float Range: 0.1 to 20
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:GATE:TIME?')
		return Conversions.str_to_float(response)

	def set_time(self, measurement_time: float) -> None:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:GATE:TIME \n
		Sets the DME analysis measurement time. \n
			:param measurement_time: float Range: 0.1 to 20
		"""
		param = Conversions.decimal_value_to_str(measurement_time)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ANALysis:GATE:TIME {param}')

	def get_length(self) -> int:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:GATE:[LENGth] \n
		Sets the gate length for the measurement window. The measurement gate settings determine the measurement window (expected
		reply delay +/- gate length/2) . Only reply pulses for which the 50% voltage point of the rising edge of the first pulse
		is within the measurement window are used to evaluate the delay time and reply efficiency. The delay measurement is
		averaged within the measurement cycle. The reply efficiency is calculated once for each measurement cycle.
		The gate length is 1 µs and the expected reply delay is 50 µs. The measurement window lies in the range between 49.5 and
		50.5 µs. Only pulse pairs are used for the measurement whose 50% voltage point of the rising edge of the first pulse is
		within this range. \n
			:return: length: integer Range: 100E-9 to 326E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:ANALysis:GATE:LENGth?')
		return Conversions.str_to_int(response)

	def set_length(self, length: int) -> None:
		"""[SOURce<HW>]:[BB]:DME:ANALysis:GATE:[LENGth] \n
		Sets the gate length for the measurement window. The measurement gate settings determine the measurement window (expected
		reply delay +/- gate length/2) . Only reply pulses for which the 50% voltage point of the rising edge of the first pulse
		is within the measurement window are used to evaluate the delay time and reply efficiency. The delay measurement is
		averaged within the measurement cycle. The reply efficiency is calculated once for each measurement cycle.
		The gate length is 1 µs and the expected reply delay is 50 µs. The measurement window lies in the range between 49.5 and
		50.5 µs. Only pulse pairs are used for the measurement whose 50% voltage point of the rising edge of the first pulse is
		within this range. \n
			:param length: integer Range: 100E-9 to 326E-6
		"""
		param = Conversions.decimal_value_to_str(length)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:ANALysis:GATE:LENGth {param}')
