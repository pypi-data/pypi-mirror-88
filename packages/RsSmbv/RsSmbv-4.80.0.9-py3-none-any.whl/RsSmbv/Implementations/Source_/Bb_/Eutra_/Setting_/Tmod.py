from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tmod:
	"""Tmod commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tmod", core, parent)

	def get_dl(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:SETTing:TMOD:DL \n
		Selects a predefined test model as defined in . \n
			:return: filename: test_model_name
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:SETTing:TMOD:DL?')
		return trim_str_response(response)

	def set_dl(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:SETTing:TMOD:DL \n
		Selects a predefined test model as defined in . \n
			:param filename: test_model_name
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:SETTing:TMOD:DL {param}')

	def get_tdd(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:SETTing:TMOD:TDD \n
		Selects a predefined test model as defined in . \n
			:return: tdd: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:SETTing:TMOD:TDD?')
		return trim_str_response(response)

	def set_tdd(self, tdd: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:SETTing:TMOD:TDD \n
		Selects a predefined test model as defined in . \n
			:param tdd: test_model_name
		"""
		param = Conversions.value_to_quoted_str(tdd)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:SETTing:TMOD:TDD {param}')
