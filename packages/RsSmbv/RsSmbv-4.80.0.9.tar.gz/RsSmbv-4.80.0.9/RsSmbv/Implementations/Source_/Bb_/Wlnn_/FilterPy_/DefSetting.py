from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DefSetting:
	"""DefSetting commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("defSetting", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:WLNN:FILTer:DEFSetting:STATe \n
		Activates the WLAN default filter settings. \n
			:return: use_default_filte: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:FILTer:DEFSetting:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, use_default_filte: bool) -> None:
		"""[SOURce<HW>]:BB:WLNN:FILTer:DEFSetting:STATe \n
		Activates the WLAN default filter settings. \n
			:param use_default_filte: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(use_default_filte)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FILTer:DEFSetting:STATe {param}')
