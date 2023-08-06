from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Waveform:
	"""Waveform commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("waveform", core, parent)

	def get_create(self) -> str:
		"""[SOURce<HW>]:BB:NR5G:WAVeform:CREate \n
		Stores the current settings as an ARB signal in a waveform file (*.wv) . Refer to 'Accessing Files in the Default or
		Specified Directory' for general information on file handling in the default and in a specific directory. \n
			:return: filename: string Filename or complete file path; file extension is assigned automatically
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:WAVeform:CREate?')
		return trim_str_response(response)

	def set_create(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:NR5G:WAVeform:CREate \n
		Stores the current settings as an ARB signal in a waveform file (*.wv) . Refer to 'Accessing Files in the Default or
		Specified Directory' for general information on file handling in the default and in a specific directory. \n
			:param filename: string Filename or complete file path; file extension is assigned automatically
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:WAVeform:CREate {param}')
