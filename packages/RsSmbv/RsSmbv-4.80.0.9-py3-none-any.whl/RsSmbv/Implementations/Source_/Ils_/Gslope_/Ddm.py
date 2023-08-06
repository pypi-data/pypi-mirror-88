from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ddm:
	"""Ddm commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ddm", core, parent)

	def get_pct(self) -> float:
		"""[SOURce<HW>]:ILS:[GSLope]:DDM:PCT \n
		Sets the difference in depth of modulation between the signal of the upper lobe (90 Hz) and the lower lobe (150 Hz) . The
		maximum value equals the sum of the modulation depths of the 90 Hz and the 150 Hz tone.
		See also [:​SOURce<hw>][:​BB]:​ILS[:​GS|GSLope]:​DDM[:​DEPTh]. \n
			:return: pct: float Range: -80.0 to 80.0
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:ILS:GSLope:DDM:PCT?')
		return Conversions.str_to_float(response)

	def set_pct(self, pct: float) -> None:
		"""[SOURce<HW>]:ILS:[GSLope]:DDM:PCT \n
		Sets the difference in depth of modulation between the signal of the upper lobe (90 Hz) and the lower lobe (150 Hz) . The
		maximum value equals the sum of the modulation depths of the 90 Hz and the 150 Hz tone.
		See also [:​SOURce<hw>][:​BB]:​ILS[:​GS|GSLope]:​DDM[:​DEPTh]. \n
			:param pct: float Range: -80.0 to 80.0
		"""
		param = Conversions.decimal_value_to_str(pct)
		self._core.io.write(f'SOURce<HwInstance>:ILS:GSLope:DDM:PCT {param}')
