from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Switching:
	"""Switching commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("switching", core, parent)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.SourceInt:
		"""[SOURce<HW>]:BB:DM:SWITching:SOURce \n
		No command help available \n
			:return: source: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:SWITching:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SourceInt)

	def set_source(self, source: enums.SourceInt) -> None:
		"""[SOURce<HW>]:BB:DM:SWITching:SOURce \n
		No command help available \n
			:param source: No help available
		"""
		param = Conversions.enum_scalar_to_str(source, enums.SourceInt)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:SWITching:SOURce {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:DM:SWITching:STATe \n
		Enables switching between a modulated and an unmodulated signal. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:SWITching:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:DM:SWITching:STATe \n
		Enables switching between a modulated and an unmodulated signal. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:SWITching:STATe {param}')
