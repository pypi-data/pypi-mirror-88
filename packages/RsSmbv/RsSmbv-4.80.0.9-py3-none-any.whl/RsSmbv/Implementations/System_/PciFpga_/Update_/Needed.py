from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Needed:
	"""Needed commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("needed", core, parent)

	def get_state(self) -> bool:
		"""SYSTem:PCIFpga:UPDate:NEEDed:[STATe] \n
		No command help available \n
			:return: update_needed: No help available
		"""
		response = self._core.io.query_str('SYSTem:PCIFpga:UPDate:NEEDed:STATe?')
		return Conversions.str_to_bool(response)
