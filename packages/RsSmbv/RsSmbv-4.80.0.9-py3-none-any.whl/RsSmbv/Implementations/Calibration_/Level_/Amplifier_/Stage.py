from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Stage:
	"""Stage commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stage", core, parent)

	def get_frequency(self) -> int:
		"""CALibration:LEVel:AMPLifier:STAGe:FREQuenz \n
		No command help available \n
			:return: freq_stage: No help available
		"""
		response = self._core.io.query_str('CALibration:LEVel:AMPLifier:STAGe:FREQuenz?')
		return Conversions.str_to_int(response)

	def set_frequency(self, freq_stage: int) -> None:
		"""CALibration:LEVel:AMPLifier:STAGe:FREQuenz \n
		No command help available \n
			:param freq_stage: No help available
		"""
		param = Conversions.decimal_value_to_str(freq_stage)
		self._core.io.write(f'CALibration:LEVel:AMPLifier:STAGe:FREQuenz {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.CalPowAmpStagMode:
		"""CALibration:LEVel:AMPLifier:STAGe:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('CALibration:LEVel:AMPLifier:STAGe:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.CalPowAmpStagMode)

	def set_mode(self, mode: enums.CalPowAmpStagMode) -> None:
		"""CALibration:LEVel:AMPLifier:STAGe:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.CalPowAmpStagMode)
		self._core.io.write(f'CALibration:LEVel:AMPLifier:STAGe:MODE {param}')

	def get_sub(self) -> int:
		"""CALibration:LEVel:AMPLifier:STAGe:SUB \n
		No command help available \n
			:return: sub_stage: No help available
		"""
		response = self._core.io.query_str('CALibration:LEVel:AMPLifier:STAGe:SUB?')
		return Conversions.str_to_int(response)

	def set_sub(self, sub_stage: int) -> None:
		"""CALibration:LEVel:AMPLifier:STAGe:SUB \n
		No command help available \n
			:param sub_stage: No help available
		"""
		param = Conversions.decimal_value_to_str(sub_stage)
		self._core.io.write(f'CALibration:LEVel:AMPLifier:STAGe:SUB {param}')

	def get_value(self) -> int:
		"""CALibration:LEVel:AMPLifier:STAGe \n
		No command help available \n
			:return: stage: No help available
		"""
		response = self._core.io.query_str('CALibration:LEVel:AMPLifier:STAGe?')
		return Conversions.str_to_int(response)

	def set_value(self, stage: int) -> None:
		"""CALibration:LEVel:AMPLifier:STAGe \n
		No command help available \n
			:param stage: No help available
		"""
		param = Conversions.decimal_value_to_str(stage)
		self._core.io.write(f'CALibration:LEVel:AMPLifier:STAGe {param}')
