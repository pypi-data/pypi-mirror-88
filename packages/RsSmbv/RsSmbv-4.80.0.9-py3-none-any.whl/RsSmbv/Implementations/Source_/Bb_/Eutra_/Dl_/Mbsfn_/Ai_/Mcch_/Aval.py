from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Aval:
	"""Aval commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aval", core, parent)

	def get(self, allocation_value: int) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:AVAL \n
		Indicates the subframes of the radio frames indicated by the 'MCCH repetition period' and the 'MCCH offset', that may
		carry MCCH. \n
			:param allocation_value: integer
			:return: allocation_value: integer"""
		param = Conversions.decimal_value_to_str(allocation_value)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:AVAL? {param}')
		return Conversions.str_to_int(response)
