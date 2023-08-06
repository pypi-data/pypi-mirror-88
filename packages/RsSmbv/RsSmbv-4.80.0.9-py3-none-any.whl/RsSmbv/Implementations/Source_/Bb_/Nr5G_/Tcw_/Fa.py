from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fa:
	"""Fa commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fa", core, parent)

	# noinspection PyTypeChecker
	def get_fr_allocation(self) -> enums.LowHigh:
		"""[SOURce<HW>]:BB:NR5G:TCW:FA:FRALlocation \n
		Sets the frequency allocation to FR1 or FR2. \n
			:return: freq_alloc: LOW| HIGH
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:FA:FRALlocation?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)

	def set_fr_allocation(self, freq_alloc: enums.LowHigh) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:FA:FRALlocation \n
		Sets the frequency allocation to FR1 or FR2. \n
			:param freq_alloc: LOW| HIGH
		"""
		param = Conversions.enum_scalar_to_str(freq_alloc, enums.LowHigh)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:FA:FRALlocation {param}')
