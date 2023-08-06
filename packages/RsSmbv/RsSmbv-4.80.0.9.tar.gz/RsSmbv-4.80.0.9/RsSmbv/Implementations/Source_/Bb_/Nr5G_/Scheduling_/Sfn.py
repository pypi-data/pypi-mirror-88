from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sfn:
	"""Sfn commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sfn", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:SCHeduling:SFN:STATe \n
		No command help available \n
			:return: sys_frame_num: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SCHeduling:SFN:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, sys_frame_num: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHeduling:SFN:STATe \n
		No command help available \n
			:param sys_frame_num: No help available
		"""
		param = Conversions.bool_to_str(sys_frame_num)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHeduling:SFN:STATe {param}')
