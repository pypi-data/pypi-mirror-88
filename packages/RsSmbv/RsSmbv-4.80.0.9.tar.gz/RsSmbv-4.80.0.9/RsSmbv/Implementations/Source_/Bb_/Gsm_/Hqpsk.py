from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hqpsk:
	"""Hqpsk commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hqpsk", core, parent)

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.GsmModTypeQpsk:
		"""[SOURce<HW>]:BB:GSM:HQPSk:FORMat \n
		The command queries the modulation type. \n
			:return: format_py: QEDGe
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:HQPSk:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.GsmModTypeQpsk)
