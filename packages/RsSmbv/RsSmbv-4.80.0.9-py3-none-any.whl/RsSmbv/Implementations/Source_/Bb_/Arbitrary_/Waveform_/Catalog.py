from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	def get_length(self) -> int:
		"""[SOURce<HW>]:BB:ARBitrary:WAVeform:CATalog:LENGth \n
		Reads out the files with extension *.wv in the default directory and returns the number of waveform files in this
		directory. The default directory is set using command method RsSmbv.MassMemory.currentDirectory. \n
			:return: length: integer Number of waveform files in default directory Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WAVeform:CATalog:LENGth?')
		return Conversions.str_to_int(response)

	def get_value(self) -> List[str]:
		"""[SOURce<HW>]:BB:ARBitrary:WAVeform:CATalog \n
		Reads out the files extension *.wv in the default directory. \n
			:return: catalog: string Returns a list of the file names separated by commas
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WAVeform:CATalog?')
		return Conversions.str_to_str_list(response)
