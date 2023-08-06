from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sweep:
	"""Sweep commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sweep", core, parent)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.SweepType:
		"""SWEep:TYPE \n
		No command help available \n
			:return: sweep_type: No help available
		"""
		response = self._core.io.query_str('SWEep:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.SweepType)

	def set_type_py(self, sweep_type: enums.SweepType) -> None:
		"""SWEep:TYPE \n
		No command help available \n
			:param sweep_type: No help available
		"""
		param = Conversions.enum_scalar_to_str(sweep_type, enums.SweepType)
		self._core.io.write(f'SWEep:TYPE {param}')
