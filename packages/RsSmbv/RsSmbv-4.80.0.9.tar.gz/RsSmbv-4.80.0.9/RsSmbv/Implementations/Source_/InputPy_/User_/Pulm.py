from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pulm:
	"""Pulm commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pulm", core, parent)

	def get_level(self) -> float:
		"""[SOURce]:INPut:USER:PULM:LEVel \n
		Sets the threshold for any input signal at the User3-5 connectors. \n
			:return: level: float Range: 0.1 to 2, Unit: V
		"""
		response = self._core.io.query_str('SOURce:INPut:USER:PULM:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""[SOURce]:INPut:USER:PULM:LEVel \n
		Sets the threshold for any input signal at the User3-5 connectors. \n
			:param level: float Range: 0.1 to 2, Unit: V
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce:INPut:USER:PULM:LEVel {param}')
