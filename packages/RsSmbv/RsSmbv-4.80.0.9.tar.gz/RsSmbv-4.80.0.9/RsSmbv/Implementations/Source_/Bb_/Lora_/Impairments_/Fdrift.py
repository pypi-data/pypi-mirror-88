from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fdrift:
	"""Fdrift commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fdrift", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:LORA:IMPairments:FDRift:STATe \n
		Activates frequency drift settings in the payload. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:IMPairments:FDRift:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:LORA:IMPairments:FDRift:STATe \n
		Activates frequency drift settings in the payload. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:IMPairments:FDRift:STATe {param}')
