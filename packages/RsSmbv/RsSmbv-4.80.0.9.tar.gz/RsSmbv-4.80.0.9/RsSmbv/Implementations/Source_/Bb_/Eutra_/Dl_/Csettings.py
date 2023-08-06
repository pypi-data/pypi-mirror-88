from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Csettings:
	"""Csettings commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("csettings", core, parent)

	def get_rarnti(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSETtings:RARNti \n
		Sets the random-access response identity RA-RNTI. The value selected here determines the value of the parameter
		'UE_ID/n_RNTI' in case a RA_RNTI 'User' is selected. \n
			:return: ra_rnti: integer Range: 1 to 60
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:CSETtings:RARNti?')
		return Conversions.str_to_int(response)

	def set_rarnti(self, ra_rnti: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CSETtings:RARNti \n
		Sets the random-access response identity RA-RNTI. The value selected here determines the value of the parameter
		'UE_ID/n_RNTI' in case a RA_RNTI 'User' is selected. \n
			:param ra_rnti: integer Range: 1 to 60
		"""
		param = Conversions.decimal_value_to_str(ra_rnti)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CSETtings:RARNti {param}')
