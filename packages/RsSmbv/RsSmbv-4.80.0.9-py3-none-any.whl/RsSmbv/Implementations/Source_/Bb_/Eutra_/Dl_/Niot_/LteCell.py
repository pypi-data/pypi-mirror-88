from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LteCell:
	"""LteCell commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lteCell", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:LTECell:STATe \n
		In in-band mode, defines how the LTE channels are handled. If enabled, all LTE channels are deactivated. However, LTE
		reference signals are still transmitted. \n
			:return: lte_cell: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:LTECell:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, lte_cell: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:LTECell:STATe \n
		In in-band mode, defines how the LTE channels are handled. If enabled, all LTE channels are deactivated. However, LTE
		reference signals are still transmitted. \n
			:param lte_cell: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(lte_cell)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:LTECell:STATe {param}')
