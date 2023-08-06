from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cosine:
	"""Cosine commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cosine", core, parent)

	def get_cofs(self) -> float:
		"""[SOURce<HW>]:BB:WLNN:FILTer:PARameter:COSine:COFS \n
		(for system bandwidth set to 20 MHz only) The command sets the 'cut of frequency shift' value for the Cosine filter type. \n
			:return: co_fs: float Range: -1 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:COSine:COFS?')
		return Conversions.str_to_float(response)

	def set_cofs(self, co_fs: float) -> None:
		"""[SOURce<HW>]:BB:WLNN:FILTer:PARameter:COSine:COFS \n
		(for system bandwidth set to 20 MHz only) The command sets the 'cut of frequency shift' value for the Cosine filter type. \n
			:param co_fs: float Range: -1 to 1
		"""
		param = Conversions.decimal_value_to_str(co_fs)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:COSine:COFS {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:BB:WLNN:FILTer:PARameter:COSine \n
		(for system bandwidth set to 20 MHz only) Sets the roll-off factor for the cosine filter type. \n
			:return: cosine: float Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:COSine?')
		return Conversions.str_to_float(response)

	def set_value(self, cosine: float) -> None:
		"""[SOURce<HW>]:BB:WLNN:FILTer:PARameter:COSine \n
		(for system bandwidth set to 20 MHz only) Sets the roll-off factor for the cosine filter type. \n
			:param cosine: float Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(cosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FILTer:PARameter:COSine {param}')
