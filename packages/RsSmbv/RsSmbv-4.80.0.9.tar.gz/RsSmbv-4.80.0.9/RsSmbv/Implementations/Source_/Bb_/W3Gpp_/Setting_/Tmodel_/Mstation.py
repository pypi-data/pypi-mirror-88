from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mstation:
	"""Mstation commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mstation", core, parent)

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:TMODel:MSTation:CATalog \n
		The command queries the list of non-standardized test models for the uplink. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:SETTing:TMODel:MSTation:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> str:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:TMODel:MSTation \n
		he command selects a test model that is not defined by the standard for the uplink. \n
			:return: mstation: string DPCCH_DPDCH_60ksps Preset, Uplink, UE1 on, DPDCH + DPCCH, Overall symbol rate 60 ksps. DPCCH_DPDCH960ksps Preset, Uplink, UE1 on, DPDCH + DPCCH, Overall symbol rate 960 ksps TS34121_R6_Table_C_10_1_4_Subtest4 Uplink test model according to 3GPP TS 34.121 Release 6, Table C.10.1.4. TS34121_R8_Table_C_10_1_4_Subtest3 Uplink test models for transmitter characteristics tests with HS-DPCCH according to 3GPP TS 34.121 Release 8, Table C.10.1.4. TS34121_R8_Table_C_11_1_3_Subtest2 Uplink test models for transmitter characteristics tests with HS-DPCCH and E-DCH according to 3GPP TS 34.121 Release 8, Table C.11.1.3. TS34121_R8_Table_C_11_1_4_Subtest1 Uplink test model for transmitter characteristics tests with HS-DPCCH and E-DCH with 16QAM according to 3GPP TS 34.121 Release 8, Table C.11.1.4.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:SETTing:TMODel:MSTation?')
		return trim_str_response(response)

	def set_value(self, mstation: str) -> None:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:TMODel:MSTation \n
		he command selects a test model that is not defined by the standard for the uplink. \n
			:param mstation: string DPCCH_DPDCH_60ksps Preset, Uplink, UE1 on, DPDCH + DPCCH, Overall symbol rate 60 ksps. DPCCH_DPDCH960ksps Preset, Uplink, UE1 on, DPDCH + DPCCH, Overall symbol rate 960 ksps TS34121_R6_Table_C_10_1_4_Subtest4 Uplink test model according to 3GPP TS 34.121 Release 6, Table C.10.1.4. TS34121_R8_Table_C_10_1_4_Subtest3 Uplink test models for transmitter characteristics tests with HS-DPCCH according to 3GPP TS 34.121 Release 8, Table C.10.1.4. TS34121_R8_Table_C_11_1_3_Subtest2 Uplink test models for transmitter characteristics tests with HS-DPCCH and E-DCH according to 3GPP TS 34.121 Release 8, Table C.11.1.3. TS34121_R8_Table_C_11_1_4_Subtest1 Uplink test model for transmitter characteristics tests with HS-DPCCH and E-DCH with 16QAM according to 3GPP TS 34.121 Release 8, Table C.11.1.4.
		"""
		param = Conversions.value_to_quoted_str(mstation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:SETTing:TMODel:MSTation {param}')
