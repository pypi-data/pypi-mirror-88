from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class N32Qam:
	"""N32Qam commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("n32Qam", core, parent)

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.GsmModType32Qam:
		"""[SOURce<HW>]:BB:GSM:N32Qam:FORMat \n
		The command queries the modulation type. \n
			:return: format_py: QAM32EDge
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:N32Qam:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.GsmModType32Qam)
