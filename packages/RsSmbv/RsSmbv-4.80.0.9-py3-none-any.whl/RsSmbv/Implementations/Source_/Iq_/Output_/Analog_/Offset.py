from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Offset:
	"""Offset commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("offset", core, parent)

	def get_icomponent(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:OFFSet:I \n
		Sets an offset Voffset between the inverting and non-inverting input of the differential analog I/Q output signal.
		The value range is adjusted so that the maximum overall output voltage does not exceed 4V, see 'Maximum overall output
		voltage'. \n
			:return: ipart: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:OFFSet:I?')
		return Conversions.str_to_float(response)

	def set_icomponent(self, ipart: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:OFFSet:I \n
		Sets an offset Voffset between the inverting and non-inverting input of the differential analog I/Q output signal.
		The value range is adjusted so that the maximum overall output voltage does not exceed 4V, see 'Maximum overall output
		voltage'. \n
			:param ipart: float Range: -0.3V to 0.3V , Unit: V
		"""
		param = Conversions.decimal_value_to_str(ipart)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:OFFSet:I {param}')

	def get_qcomponent(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:OFFSet:Q \n
		Sets an offset Voffset between the inverting and non-inverting input of the differential analog I/Q output signal.
		The value range is adjusted so that the maximum overall output voltage does not exceed 4V, see 'Maximum overall output
		voltage'. \n
			:return: qpart: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:OFFSet:Q?')
		return Conversions.str_to_float(response)

	def set_qcomponent(self, qpart: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:OFFSet:Q \n
		Sets an offset Voffset between the inverting and non-inverting input of the differential analog I/Q output signal.
		The value range is adjusted so that the maximum overall output voltage does not exceed 4V, see 'Maximum overall output
		voltage'. \n
			:param qpart: float Range: -0.3V to 0.3V , Unit: V
		"""
		param = Conversions.decimal_value_to_str(qpart)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:OFFSet:Q {param}')
