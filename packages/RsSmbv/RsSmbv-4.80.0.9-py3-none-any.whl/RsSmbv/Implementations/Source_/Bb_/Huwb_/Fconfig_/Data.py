from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def get_dselection(self) -> str:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:DATA:DSELection \n
		Selects an existing data list file from the default directory or from the specific directory. The data list is only used,
		if the DLIS is selected. \n
			:return: dselection: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:DATA:DSELection?')
		return trim_str_response(response)

	def set_dselection(self, dselection: str) -> None:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:DATA:DSELection \n
		Selects an existing data list file from the default directory or from the specific directory. The data list is only used,
		if the DLIS is selected. \n
			:param dselection: string
		"""
		param = Conversions.value_to_quoted_str(dselection)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:DATA:DSELection {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.HrpUwbDataSource:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:DATA \n
		Sets the data source for the payload data in a frame. \n
			:return: data_source: PN9| PN11| PN15| PN20| PN16| PN21| PN23| ONE| ZERO
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:DATA?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbDataSource)

	def set_value(self, data_source: enums.HrpUwbDataSource) -> None:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:DATA \n
		Sets the data source for the payload data in a frame. \n
			:param data_source: PN9| PN11| PN15| PN20| PN16| PN21| PN23| ONE| ZERO
		"""
		param = Conversions.enum_scalar_to_str(data_source, enums.HrpUwbDataSource)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:DATA {param}')
