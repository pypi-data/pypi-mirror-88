from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Detatt:
	"""Detatt commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("detatt", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.CalPowAmpDetMode:
		"""CALibration:LEVel:DETatt:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('CALibration:LEVel:DETatt:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.CalPowAmpDetMode)

	def set_mode(self, mode: enums.CalPowAmpDetMode) -> None:
		"""CALibration:LEVel:DETatt:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.CalPowAmpDetMode)
		self._core.io.write(f'CALibration:LEVel:DETatt:MODE {param}')
