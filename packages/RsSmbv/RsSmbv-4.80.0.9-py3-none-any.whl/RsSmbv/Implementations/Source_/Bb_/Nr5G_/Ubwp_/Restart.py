from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Restart:
	"""Restart commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("restart", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:UBWP:RESTart:STATe \n
		No command help available \n
			:return: restart_data_stat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:UBWP:RESTart:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, restart_data_stat: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:RESTart:STATe \n
		No command help available \n
			:param restart_data_stat: No help available
		"""
		param = Conversions.bool_to_str(restart_data_stat)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:RESTart:STATe {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.RestartDataAll:
		"""[SOURce<HW>]:BB:NR5G:UBWP:RESTart \n
		Sets the parameter for restarting the configured data sources in customized DCIs. \n
			:return: restart_data_sel: OFF| COAL| FRAMe OFF Disables the restart of data and control. Data sources are initialized only once at the start of the generated signal. COAL Enables the restart of data and control after each codeword and allocation. For example, the same payload is used for repeated allocations. FRAMe Enables the restart of data and control after each frame. For example, the same payload is used for allocations which are repeated each frame.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:UBWP:RESTart?')
		return Conversions.str_to_scalar_enum(response, enums.RestartDataAll)

	def set_value(self, restart_data_sel: enums.RestartDataAll) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:RESTart \n
		Sets the parameter for restarting the configured data sources in customized DCIs. \n
			:param restart_data_sel: OFF| COAL| FRAMe OFF Disables the restart of data and control. Data sources are initialized only once at the start of the generated signal. COAL Enables the restart of data and control after each codeword and allocation. For example, the same payload is used for repeated allocations. FRAMe Enables the restart of data and control after each frame. For example, the same payload is used for allocations which are repeated each frame.
		"""
		param = Conversions.enum_scalar_to_str(restart_data_sel, enums.RestartDataAll)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:RESTart {param}')
