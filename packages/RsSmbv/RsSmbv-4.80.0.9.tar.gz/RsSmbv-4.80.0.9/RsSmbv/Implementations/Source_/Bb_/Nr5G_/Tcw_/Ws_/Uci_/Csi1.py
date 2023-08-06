from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Csi1:
	"""Csi1 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("csi1", core, parent)

	def get_pattern(self) -> List[str]:
		"""[SOURce<HW>]:BB:NR5G:TCW:WS:UCI:CSI1:PATTern \n
		Defines the frequency and time domain of the CSI part 1 subcarrier location. \n
			:return: csi_1_pattern: Nr5gPUCCHUcidataPattLenMax bits
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:UCI:CSI1:PATTern?')
		return Conversions.str_to_str_list(response)

	def set_pattern(self, csi_1_pattern: List[str]) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:WS:UCI:CSI1:PATTern \n
		Defines the frequency and time domain of the CSI part 1 subcarrier location. \n
			:param csi_1_pattern: Nr5gPUCCHUcidataPattLenMax bits
		"""
		param = Conversions.list_to_csv_str(csi_1_pattern)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:UCI:CSI1:PATTern {param}')
