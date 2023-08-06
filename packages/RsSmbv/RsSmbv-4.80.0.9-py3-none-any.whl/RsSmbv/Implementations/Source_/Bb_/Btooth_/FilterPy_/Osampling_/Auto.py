from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Auto:
	"""Auto commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("auto", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:BTOoth:FILTer:OSAMpling:AUTO:[STATe] \n
		Activates the upsampling factor state. If activated, the most sensible parameter values are selected. The value depends
		on the coherence check. If deactivated, the values can be changed manually. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:FILTer:OSAMpling:AUTO:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:BTOoth:FILTer:OSAMpling:AUTO:[STATe] \n
		Activates the upsampling factor state. If activated, the most sensible parameter values are selected. The value depends
		on the coherence check. If deactivated, the values can be changed manually. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:FILTer:OSAMpling:AUTO:STATe {param}')
