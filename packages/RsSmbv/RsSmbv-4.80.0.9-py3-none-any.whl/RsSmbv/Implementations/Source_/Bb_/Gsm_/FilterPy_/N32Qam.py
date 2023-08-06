from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class N32Qam:
	"""N32Qam commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("n32Qam", core, parent)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.GilterEdge:
		"""[SOURce<HW>]:BB:GSM:FILTer:N32Qam:TYPE \n
		Queries filter for 32QAM signal. The filter is permanently set to GAUSS linearized. \n
			:return: type_py: LGAuss
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:FILTer:N32Qam:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.GilterEdge)
