from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dattenuator:
	"""Dattenuator commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dattenuator", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:SWEep:POWer:DATTenuator:STATe \n
		No command help available \n
			:return: dattstate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:DATTenuator:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, dattstate: bool) -> None:
		"""[SOURce<HW>]:SWEep:POWer:DATTenuator:STATe \n
		No command help available \n
			:param dattstate: No help available
		"""
		param = Conversions.bool_to_str(dattstate)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:DATTenuator:STATe {param}')
