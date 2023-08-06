from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class N16Qam:
	"""N16Qam commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("n16Qam", core, parent)

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.GsmModType16Qam:
		"""[SOURce<HW>]:BB:GSM:N16Qam:FORMat \n
		The command queries the modulation type. \n
			:return: format_py: QAM16EDge
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:N16Qam:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.GsmModType16Qam)
