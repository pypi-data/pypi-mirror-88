from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FpFpga:
	"""FpFpga commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fpFpga", core, parent)

	def set_update(self, display_size: str) -> None:
		"""SYSTem:FPFPga:UPDate \n
		No command help available \n
			:param display_size: No help available
		"""
		param = Conversions.value_to_quoted_str(display_size)
		self._core.io.write(f'SYSTem:FPFPga:UPDate {param}')
