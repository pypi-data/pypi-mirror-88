from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Step:
	"""Step commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("step", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FreqStepMode:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:POWer:STEP:MODE \n
		Defines the type of step size to vary the digital output power step-by-step. \n
			:return: mode: DECimal| USER DECimal increases or decreases the level in steps of ten. USER increases or decreases the level in increments, determined with the command IQ:OUTPut:DIGital:POWer.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:DIGital:POWer:STEP:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FreqStepMode)

	def set_mode(self, mode: enums.FreqStepMode) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:POWer:STEP:MODE \n
		Defines the type of step size to vary the digital output power step-by-step. \n
			:param mode: DECimal| USER DECimal increases or decreases the level in steps of ten. USER increases or decreases the level in increments, determined with the command IQ:OUTPut:DIGital:POWer.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FreqStepMode)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:DIGital:POWer:STEP:MODE {param}')

	def get_increment(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:POWer:STEP:[INCRement] \n
		Sets the step width. Use this value to vary the digital I/Q output level step-by-step. \n
			:return: ipartncrement: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:DIGital:POWer:STEP:INCRement?')
		return Conversions.str_to_float(response)

	def set_increment(self, ipartncrement: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:POWer:STEP:[INCRement] \n
		Sets the step width. Use this value to vary the digital I/Q output level step-by-step. \n
			:param ipartncrement: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(ipartncrement)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:DIGital:POWer:STEP:INCRement {param}')
