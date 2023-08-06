from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AqPsk:
	"""AqPsk commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aqPsk", core, parent)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.GilterEdge:
		"""[SOURce<HW>]:BB:GSM:FILTer:AQPSK:TYPE \n
		Queries the filter type for AQPSK modulation. The filter is permanently set to GAUSS linearized. \n
			:return: type_py: LGAuss
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:FILTer:AQPSK:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.GilterEdge)
