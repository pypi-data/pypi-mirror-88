from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Quadrature:
	"""Quadrature commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("quadrature", core, parent)

	def get_angle(self) -> float:
		"""[SOURce]:BB:IMPairment:DIGital:QUADrature:[ANGLe] \n
		Sets a quadrature offset (phase angle) between the I and Q vectors deviating from the ideal 90 degrees.
		A positive quadrature offset results in a phase angle greater than 90 degrees. Value range
			Table Header: Impairments / Min [dB] / Max [dB] / Resolution \n
			- Digital / 30 / 30 / 0.01
			- Analog / 10 / 10 / 0.01 \n
			:return: angle: float Range: -30 to 30, Unit: DEG
		"""
		response = self._core.io.query_str('SOURce:BB:IMPairment:DIGital:QUADrature:ANGLe?')
		return Conversions.str_to_float(response)

	def set_angle(self, angle: float) -> None:
		"""[SOURce]:BB:IMPairment:DIGital:QUADrature:[ANGLe] \n
		Sets a quadrature offset (phase angle) between the I and Q vectors deviating from the ideal 90 degrees.
		A positive quadrature offset results in a phase angle greater than 90 degrees. Value range
			Table Header: Impairments / Min [dB] / Max [dB] / Resolution \n
			- Digital / 30 / 30 / 0.01
			- Analog / 10 / 10 / 0.01 \n
			:param angle: float Range: -30 to 30, Unit: DEG
		"""
		param = Conversions.decimal_value_to_str(angle)
		self._core.io.write(f'SOURce:BB:IMPairment:DIGital:QUADrature:ANGLe {param}')
