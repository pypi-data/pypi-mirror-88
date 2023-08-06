from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tprs:
	"""Tprs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tprs", core, parent)

	def get(self, periodicity_tprs: int) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:PRSS:TPRS \n
		Queries the periodicity of the PRS generation (TPRS) as defined in 3GPP TS 36.211, table 6.10.4.3-1. \n
			:param periodicity_tprs: integer Range: 160 to 1280
			:return: periodicity_tprs: integer Range: 160 to 1280"""
		param = Conversions.decimal_value_to_str(periodicity_tprs)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:PRSS:TPRS? {param}')
		return Conversions.str_to_int(response)
