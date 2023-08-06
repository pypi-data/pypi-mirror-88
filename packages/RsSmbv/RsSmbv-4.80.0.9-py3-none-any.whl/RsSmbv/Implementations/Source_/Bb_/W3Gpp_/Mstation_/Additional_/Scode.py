from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scode:
	"""Scode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scode", core, parent)

	def get_step(self) -> List[str]:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:SCODe:STEP \n
		Sets the step width for increasing the scrambling code of the additional user equipment. The start value is the
		scrambling code of UE4. \n
			:return: step: integer Range: 0 to #HFFFFFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:SCODe:STEP?')
		return Conversions.str_to_str_list(response)

	def set_step(self, step: List[str]) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ADDitional:SCODe:STEP \n
		Sets the step width for increasing the scrambling code of the additional user equipment. The start value is the
		scrambling code of UE4. \n
			:param step: integer Range: 0 to #HFFFFFF
		"""
		param = Conversions.list_to_csv_str(step)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ADDitional:SCODe:STEP {param}')
