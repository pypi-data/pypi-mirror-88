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
		"""[SOURce<HW>]:BB:DAB:FILTer:PARameter:COSine:COFS \n
		No command help available \n
			:return: cofs: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:FILTer:PARameter:COSine:COFS?')
		return Conversions.str_to_float(response)

	def set_cofs(self, cofs: float) -> None:
		"""[SOURce<HW>]:BB:DAB:FILTer:PARameter:COSine:COFS \n
		No command help available \n
			:param cofs: No help available
		"""
		param = Conversions.decimal_value_to_str(cofs)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:FILTer:PARameter:COSine:COFS {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:BB:DAB:FILTer:PARameter:COSine \n
		No command help available \n
			:return: cosine: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:FILTer:PARameter:COSine?')
		return Conversions.str_to_float(response)

	def set_value(self, cosine: float) -> None:
		"""[SOURce<HW>]:BB:DAB:FILTer:PARameter:COSine \n
		No command help available \n
			:param cosine: No help available
		"""
		param = Conversions.decimal_value_to_str(cosine)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:FILTer:PARameter:COSine {param}')
