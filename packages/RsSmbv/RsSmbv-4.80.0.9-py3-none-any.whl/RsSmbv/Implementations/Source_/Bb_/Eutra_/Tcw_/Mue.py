from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mue:
	"""Mue commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mue", core, parent)

	def get_ovrb(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:MUE:OVRB \n
		Sets the number of RB the allocated RB(s) are shifted with. \n
			:return: offset_vrb: integer Range: 0 to 75
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:MUE:OVRB?')
		return Conversions.str_to_int(response)

	def set_ovrb(self, offset_vrb: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:MUE:OVRB \n
		Sets the number of RB the allocated RB(s) are shifted with. \n
			:param offset_vrb: integer Range: 0 to 75
		"""
		param = Conversions.decimal_value_to_str(offset_vrb)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:MUE:OVRB {param}')

	def get_tsrs(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:TCW:MUE:TSRS \n
		No command help available \n
			:return: transmit_srs: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:MUE:TSRS?')
		return Conversions.str_to_bool(response)

	def set_tsrs(self, transmit_srs: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:MUE:TSRS \n
		No command help available \n
			:param transmit_srs: No help available
		"""
		param = Conversions.bool_to_str(transmit_srs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:MUE:TSRS {param}')

	def get_ueid(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TCW:MUE:UEID \n
		Sets the UE ID/n_RNTI. \n
			:return: ue_id_nrnti: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:MUE:UEID?')
		return Conversions.str_to_int(response)

	def set_ueid(self, ue_id_nrnti: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:MUE:UEID \n
		Sets the UE ID/n_RNTI. \n
			:param ue_id_nrnti: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(ue_id_nrnti)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:MUE:UEID {param}')
