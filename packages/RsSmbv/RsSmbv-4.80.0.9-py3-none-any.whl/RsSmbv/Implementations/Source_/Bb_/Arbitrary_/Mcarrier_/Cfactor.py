from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cfactor:
	"""Cfactor commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cfactor", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ArbMultCarrCresMode:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CFACtor:MODE \n
		Sets the mode for optimizing the crest factor by calculating the carrier phases. \n
			:return: mode: OFF| MIN| MAX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:CFACtor:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ArbMultCarrCresMode)

	def set_mode(self, mode: enums.ArbMultCarrCresMode) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CFACtor:MODE \n
		Sets the mode for optimizing the crest factor by calculating the carrier phases. \n
			:param mode: OFF| MIN| MAX
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ArbMultCarrCresMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CFACtor:MODE {param}')
