from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.RoscOutpFreqMode:
		"""[SOURce]:ROSCillator:OUTPut:FREQuency:MODE \n
		Selects the mode for the output reference frequency. \n
			:return: outp_freq_mode: DER10M| OFF| LOOPthrough OFF Disables the output. DER10M Sets the output reference frequency to 10 MHz. The reference frequency is derived from the internal reference frequency. LOOPthrough This option is unavailable for ROSCillator:EXTernal:FREQuency 1GHZ. Forwards the input reference frequency to the reference frequency output.
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:OUTPut:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.RoscOutpFreqMode)

	def set_mode(self, outp_freq_mode: enums.RoscOutpFreqMode) -> None:
		"""[SOURce]:ROSCillator:OUTPut:FREQuency:MODE \n
		Selects the mode for the output reference frequency. \n
			:param outp_freq_mode: DER10M| OFF| LOOPthrough OFF Disables the output. DER10M Sets the output reference frequency to 10 MHz. The reference frequency is derived from the internal reference frequency. LOOPthrough This option is unavailable for ROSCillator:EXTernal:FREQuency 1GHZ. Forwards the input reference frequency to the reference frequency output.
		"""
		param = Conversions.enum_scalar_to_str(outp_freq_mode, enums.RoscOutpFreqMode)
		self._core.io.write(f'SOURce:ROSCillator:OUTPut:FREQuency:MODE {param}')
