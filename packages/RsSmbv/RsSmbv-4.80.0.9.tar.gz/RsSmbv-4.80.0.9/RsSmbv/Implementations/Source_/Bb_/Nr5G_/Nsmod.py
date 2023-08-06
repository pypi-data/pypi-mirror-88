from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nsmod:
	"""Nsmod commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nsmod", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:NSMod:STATe \n
		No command help available \n
			:return: non_std_modualtio: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:NSMod:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, non_std_modualtio: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:NSMod:STATe \n
		No command help available \n
			:param non_std_modualtio: No help available
		"""
		param = Conversions.bool_to_str(non_std_modualtio)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NSMod:STATe {param}')
