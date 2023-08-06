from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pag:
	"""Pag commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pag", core, parent)

	# noinspection PyTypeChecker
	def get_rmax(self) -> enums.EutraNbiotRmAx:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:PAG:RMAX \n
		Sets the maximum number NPDCCH is repeated RMax (paging) . \n
			:return: paging_rmax: R1| R2| R4| R8| R16| R32| R64| R128| R256| R512| R1024| R2048
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:PAG:RMAX?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotRmAx)

	def set_rmax(self, paging_rmax: enums.EutraNbiotRmAx) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:PAG:RMAX \n
		Sets the maximum number NPDCCH is repeated RMax (paging) . \n
			:param paging_rmax: R1| R2| R4| R8| R16| R32| R64| R128| R256| R512| R1024| R2048
		"""
		param = Conversions.enum_scalar_to_str(paging_rmax, enums.EutraNbiotRmAx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:PAG:RMAX {param}')
