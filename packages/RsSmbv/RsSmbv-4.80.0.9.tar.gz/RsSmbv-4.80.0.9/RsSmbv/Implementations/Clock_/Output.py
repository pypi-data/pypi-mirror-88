from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ClocOutpMode:
		"""CLOCk:OUTPut:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('CLOCk:OUTPut:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ClocOutpMode)

	def set_mode(self, mode: enums.ClocOutpMode) -> None:
		"""CLOCk:OUTPut:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ClocOutpMode)
		self._core.io.write(f'CLOCk:OUTPut:MODE {param}')
