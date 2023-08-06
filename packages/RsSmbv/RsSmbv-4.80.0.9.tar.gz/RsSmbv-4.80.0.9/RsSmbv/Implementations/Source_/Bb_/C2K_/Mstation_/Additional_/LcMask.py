from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LcMask:
	"""LcMask commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lcMask", core, parent)

	def get_step(self) -> List[str]:
		"""[SOURce<HW>]:BB:C2K:MSTation:ADDitional:LCMask:STEP \n
		Sets the step width for increasing the LC mask of the additional mobile stations. The start value is the LC mask of MS4. \n
			:return: step: 24 bits
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:MSTation:ADDitional:LCMask:STEP?')
		return Conversions.str_to_str_list(response)

	def set_step(self, step: List[str]) -> None:
		"""[SOURce<HW>]:BB:C2K:MSTation:ADDitional:LCMask:STEP \n
		Sets the step width for increasing the LC mask of the additional mobile stations. The start value is the LC mask of MS4. \n
			:param step: 24 bits
		"""
		param = Conversions.list_to_csv_str(step)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation:ADDitional:LCMask:STEP {param}')
