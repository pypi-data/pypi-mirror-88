from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sequence:
	"""Sequence commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sequence", core, parent)

	def get_select(self) -> str:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:SEQuence:SELect \n
		Selects the sequencing list (files with extension *.wvs) \n
			:return: filename: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:SEQuence:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:SEQuence:SELect \n
		Selects the sequencing list (files with extension *.wvs) \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:SEQuence:SELect {param}')
