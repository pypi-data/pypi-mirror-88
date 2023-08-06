from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Step:
	"""Step commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("step", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FreqStepMode:
		"""[SOURce<HW>]:POWer:STEP:MODE \n
		Defines the type of step width to vary the RF output power step-by-step with the commands POW UP or POW DOWN. \n
			:return: mode: DECimal| USER DECimal Increases or decreases the level in steps of ten. USER Increases or decreases the level in increments, determined with the command method RsSmbv.Source.Power.Level.Immediate.amplitude.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:STEP:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FreqStepMode)

	def set_mode(self, mode: enums.FreqStepMode) -> None:
		"""[SOURce<HW>]:POWer:STEP:MODE \n
		Defines the type of step width to vary the RF output power step-by-step with the commands POW UP or POW DOWN. \n
			:param mode: DECimal| USER DECimal Increases or decreases the level in steps of ten. USER Increases or decreases the level in increments, determined with the command method RsSmbv.Source.Power.Level.Immediate.amplitude.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FreqStepMode)
		self._core.io.write(f'SOURce<HwInstance>:POWer:STEP:MODE {param}')

	def get_increment(self) -> float:
		"""[SOURce<HW>]:POWer:STEP:[INCRement] \n
		Specifies the step width in the appropriate path for POW:STEP:MODE USER. To adjust the level step-by-step with this
		increment value, use the command POW UP, or POW DOWN. Note: The command also sets 'Variation Step' in the manual control,
		that means the user-defined step width for setting the level with the rotary knob or the [Up/Down] arrow keys. \n
			:return: increment: float Range: 0 to 200, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:STEP:INCRement?')
		return Conversions.str_to_float(response)

	def set_increment(self, increment: float) -> None:
		"""[SOURce<HW>]:POWer:STEP:[INCRement] \n
		Specifies the step width in the appropriate path for POW:STEP:MODE USER. To adjust the level step-by-step with this
		increment value, use the command POW UP, or POW DOWN. Note: The command also sets 'Variation Step' in the manual control,
		that means the user-defined step width for setting the level with the rotary knob or the [Up/Down] arrow keys. \n
			:param increment: float Range: 0 to 200, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(increment)
		self._core.io.write(f'SOURce<HwInstance>:POWer:STEP:INCRement {param}')
