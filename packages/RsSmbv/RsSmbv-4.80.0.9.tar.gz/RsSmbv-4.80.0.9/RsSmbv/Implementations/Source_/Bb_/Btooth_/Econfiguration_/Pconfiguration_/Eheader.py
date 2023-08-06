from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Eheader:
	"""Eheader commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eheader", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:EHEader:STATe \n
		Enables / disables extended header for advertising packets with scanning PDUs. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:EHEader:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:EHEader:STATe \n
		Enables / disables extended header for advertising packets with scanning PDUs. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:EHEader:STATe {param}')
