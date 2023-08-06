from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Noise:
	"""Noise commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("noise", core, parent)

	def get_total(self) -> float:
		"""[SOURce<HW>]:AWGN:POWer:NOISe:TOTal \n
		Queries the noise level in the total bandwidth. \n
			:return: total: float Range: -145 to 20
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:POWer:NOISe:TOTal?')
		return Conversions.str_to_float(response)

	def get_value(self) -> float:
		"""[SOURce<HW>]:AWGN:POWer:NOISe \n
		Sets the power of the noise signal in the system respectively total bandwidth. \n
			:return: noise: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:POWer:NOISe?')
		return Conversions.str_to_float(response)

	def set_value(self, noise: float) -> None:
		"""[SOURce<HW>]:AWGN:POWer:NOISe \n
		Sets the power of the noise signal in the system respectively total bandwidth. \n
			:param noise: float
		"""
		param = Conversions.decimal_value_to_str(noise)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:POWer:NOISe {param}')
