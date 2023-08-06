from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Step:
	"""Step commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("step", core, parent)

	def get_logarithmic(self) -> float:
		"""[SOURce<HW>]:SWEep:POWer:STEP:[LOGarithmic] \n
		Sets a logarithmically determined step size for the RF level sweep. The level is increased by a logarithmically
		calculated fraction of the current level. See 'Correlating Parameters in Sweep Mode'. \n
			:return: logarithmic: float The unit dB is mandatory. Range: 0.01 to 139 dB, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:STEP:LOGarithmic?')
		return Conversions.str_to_float(response)

	def set_logarithmic(self, logarithmic: float) -> None:
		"""[SOURce<HW>]:SWEep:POWer:STEP:[LOGarithmic] \n
		Sets a logarithmically determined step size for the RF level sweep. The level is increased by a logarithmically
		calculated fraction of the current level. See 'Correlating Parameters in Sweep Mode'. \n
			:param logarithmic: float The unit dB is mandatory. Range: 0.01 to 139 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(logarithmic)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:STEP:LOGarithmic {param}')
