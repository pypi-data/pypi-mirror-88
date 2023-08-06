from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.Rosc1GoUtpFreqMode:
		"""[SOURce]:ROSCillator:OUTPut:ALTernate:FREQuency:MODE \n
		Sets the output reference frequency. \n
			:return: outp_freq_mode: LOOPthrough| DER1G| OFF OFF Disables the output. DER1G Sets the output reference frequency to 1 GHz. The reference frequency is derived from the internal reference frequency. LOOPthrough If method RsSmbv.Source.Roscillator.External.Frequency.value1GHZ, forwards the input reference frequency to the reference frequency output.
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:OUTPut:ALTernate:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.Rosc1GoUtpFreqMode)

	def set_mode(self, outp_freq_mode: enums.Rosc1GoUtpFreqMode) -> None:
		"""[SOURce]:ROSCillator:OUTPut:ALTernate:FREQuency:MODE \n
		Sets the output reference frequency. \n
			:param outp_freq_mode: LOOPthrough| DER1G| OFF OFF Disables the output. DER1G Sets the output reference frequency to 1 GHz. The reference frequency is derived from the internal reference frequency. LOOPthrough If method RsSmbv.Source.Roscillator.External.Frequency.value1GHZ, forwards the input reference frequency to the reference frequency output.
		"""
		param = Conversions.enum_scalar_to_str(outp_freq_mode, enums.Rosc1GoUtpFreqMode)
		self._core.io.write(f'SOURce:ROSCillator:OUTPut:ALTernate:FREQuency:MODE {param}')
