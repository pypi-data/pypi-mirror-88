from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Apsk16:
	"""Apsk16 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apsk16", core, parent)

	# noinspection PyTypeChecker
	def get_gamma(self) -> enums.DmApskGamma:
		"""[SOURce<HW>]:BB:DM:APSK16:GAMMa \n
		Sets the gamma function γ for the 16APSK modulation. \n
			:return: gamma: G2D3| G3D4| G4D5| G5D6| G8D9| G9D10 GxDy: G = Gamma function, xy = code rate
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:APSK16:GAMMa?')
		return Conversions.str_to_scalar_enum(response, enums.DmApskGamma)

	def set_gamma(self, gamma: enums.DmApskGamma) -> None:
		"""[SOURce<HW>]:BB:DM:APSK16:GAMMa \n
		Sets the gamma function γ for the 16APSK modulation. \n
			:param gamma: G2D3| G3D4| G4D5| G5D6| G8D9| G9D10 GxDy: G = Gamma function, xy = code rate
		"""
		param = Conversions.enum_scalar_to_str(gamma, enums.DmApskGamma)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:APSK16:GAMMa {param}')
