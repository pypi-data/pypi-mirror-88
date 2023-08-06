from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Snos:
	"""Snos commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("snos", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:FEAT:SNOS:STATe \n
		No command help available \n
			:return: separate_num_outp: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:FEAT:SNOS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, separate_num_outp: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:FEAT:SNOS:STATe \n
		No command help available \n
			:param separate_num_outp: No help available
		"""
		param = Conversions.bool_to_str(separate_num_outp)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:FEAT:SNOS:STATe {param}')
