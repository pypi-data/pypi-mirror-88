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
		"""[SOURce<HW>]:BB:TDSCdma:WAVeform:CREate \n
		Stores the current settings as an ARB signal in a waveform file (*.wv) . For general information on file handling in the
		default and in a specific directory, see section 'MMEMory Subsystem' in the R&S SMBVB operating manual. \n
			:param filename: string Filename or complete file path; file extension is assigned automatically
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:WAVeform:CREate {param}')
