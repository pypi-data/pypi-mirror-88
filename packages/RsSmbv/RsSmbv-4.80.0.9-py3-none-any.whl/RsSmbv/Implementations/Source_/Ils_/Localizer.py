from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Localizer:
	"""Localizer commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("localizer", core, parent)

	def preset(self) -> None:
		"""[SOURce<HW>]:ILS:LOCalizer:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:ILS:LOCalizer:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:ILS:LOCalizer:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:ILS:LOCalizer:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:LOCalizer:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:ILS:LOCalizer:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:ILS:LOCalizer:STATe {param}')
