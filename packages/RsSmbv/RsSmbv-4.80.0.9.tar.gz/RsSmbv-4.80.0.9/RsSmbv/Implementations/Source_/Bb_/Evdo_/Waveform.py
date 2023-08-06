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
		"""[SOURce<HW>]:BB:EVDO:WAVeform:CREate \n
		Creates a waveform using the current settings. The file is stored with the predefined file extension *.wv. The filename
		and the directory it is stored in are user-definable. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:WAVeform:CREate {param}')
