from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Niot:
	"""Niot commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("niot", core, parent)

	def get_power(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:REFSig:NIOT:POWer \n
		Sets the power of the narrowband reference signal (NRS) . \n
			:return: nb_ref_sig_sym_powe: float Range: -80 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:REFSig:NIOT:POWer?')
		return Conversions.str_to_float(response)

	def set_power(self, nb_ref_sig_sym_powe: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:REFSig:NIOT:POWer \n
		Sets the power of the narrowband reference signal (NRS) . \n
			:param nb_ref_sig_sym_powe: float Range: -80 to 10
		"""
		param = Conversions.decimal_value_to_str(nb_ref_sig_sym_powe)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:REFSig:NIOT:POWer {param}')
