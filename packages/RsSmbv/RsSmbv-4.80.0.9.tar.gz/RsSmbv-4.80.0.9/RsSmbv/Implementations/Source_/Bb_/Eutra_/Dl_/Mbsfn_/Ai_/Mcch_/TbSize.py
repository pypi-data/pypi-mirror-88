from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TbSize:
	"""TbSize commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tbSize", core, parent)

	def get(self, tb_size: int) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:TBSize \n
		Queries the values as determined by the 'MCCH MCS'. \n
			:param tb_size: integer
			:return: tb_size: integer"""
		param = Conversions.decimal_value_to_str(tb_size)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:TBSize? {param}')
		return Conversions.str_to_int(response)
