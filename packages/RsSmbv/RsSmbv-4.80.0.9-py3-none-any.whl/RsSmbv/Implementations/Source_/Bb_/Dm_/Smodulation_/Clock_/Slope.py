from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slope:
	"""Slope commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slope", core, parent)

	# noinspection PyTypeChecker
	def get_bit(self) -> enums.SlopeType:
		"""[SOURce<HW>]:BB:DM:SMODulation:CLOCk:SLOPe:BIT \n
		No command help available \n
			:return: slope: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:SMODulation:CLOCk:SLOPe:BIT?')
		return Conversions.str_to_scalar_enum(response, enums.SlopeType)

	def set_bit(self, slope: enums.SlopeType) -> None:
		"""[SOURce<HW>]:BB:DM:SMODulation:CLOCk:SLOPe:BIT \n
		No command help available \n
			:param slope: No help available
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.SlopeType)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:SMODulation:CLOCk:SLOPe:BIT {param}')
