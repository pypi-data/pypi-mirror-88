from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Waveform:
	"""Waveform commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("waveform", core, parent)

	def set_create(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:GBAS:WAVeform:CREate \n
		With enabled signal generation, triggers the instrument to store the current settings as an ARB signal in a waveform file.
		Waveform files can be further processed by the ARB and/or as a multi-carrier or a multi-segment signal. The filename and
		the directory it is stored in are user-definable; the predefined file extension for waveform files is *.wv. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:WAVeform:CREate {param}')
