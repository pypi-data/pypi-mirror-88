from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coder:
	"""Coder commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coder", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.BbCodMode:
		"""[SOURce<HW>]:BB:CODer:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:CODer:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.BbCodMode)

	def set_mode(self, mode: enums.BbCodMode) -> None:
		"""[SOURce<HW>]:BB:CODer:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.BbCodMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:CODer:MODE {param}')
