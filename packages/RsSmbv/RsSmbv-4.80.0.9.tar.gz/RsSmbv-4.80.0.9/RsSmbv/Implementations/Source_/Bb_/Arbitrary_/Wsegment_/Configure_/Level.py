from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Level:
	"""Level commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("level", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ArbWaveSegmPowMode:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:LEVel:[MODE] \n
		Selects the level mode, unchanged or equal RMS, for the multi-segment waveform. \n
			:return: mode: UNCHanged| ERMS
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:LEVel:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ArbWaveSegmPowMode)

	def set_mode(self, mode: enums.ArbWaveSegmPowMode) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:WSEGment:CONFigure:LEVel:[MODE] \n
		Selects the level mode, unchanged or equal RMS, for the multi-segment waveform. \n
			:param mode: UNCHanged| ERMS
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ArbWaveSegmPowMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:WSEGment:CONFigure:LEVel:MODE {param}')
