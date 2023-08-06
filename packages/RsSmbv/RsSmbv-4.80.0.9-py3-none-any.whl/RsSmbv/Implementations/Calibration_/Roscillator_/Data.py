from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.CalDataMode:
		"""CALibration:ROSCillator:DATA:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('CALibration:ROSCillator:DATA:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.CalDataMode)

	def set_mode(self, mode: enums.CalDataMode) -> None:
		"""CALibration:ROSCillator:DATA:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.CalDataMode)
		self._core.io.write(f'CALibration:ROSCillator:DATA:MODE {param}')

	def get_value(self) -> int:
		"""CALibration:ROSCillator:[DATA] \n
		No command help available \n
			:return: data: No help available
		"""
		response = self._core.io.query_str('CALibration:ROSCillator:DATA?')
		return Conversions.str_to_int(response)

	def set_value(self, data: int) -> None:
		"""CALibration:ROSCillator:[DATA] \n
		No command help available \n
			:param data: No help available
		"""
		param = Conversions.decimal_value_to_str(data)
		self._core.io.write(f'CALibration:ROSCillator:DATA {param}')
