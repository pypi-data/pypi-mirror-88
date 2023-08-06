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
		"""[SOURce<HW>]:FREQuency:STEP:MODE \n
		Defines the type of step size to vary the RF frequency at discrete steps with the commands FREQ UP or FREQ DOWN. \n
			:return: mode: DECimal| USER DECimal Increases or decreases the level in steps of ten. USER Increases or decreases the level in increments, set with the command method RsSmbv.Source.Frequency.Step.increment.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:STEP:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FreqStepMode)

	def set_mode(self, mode: enums.FreqStepMode) -> None:
		"""[SOURce<HW>]:FREQuency:STEP:MODE \n
		Defines the type of step size to vary the RF frequency at discrete steps with the commands FREQ UP or FREQ DOWN. \n
			:param mode: DECimal| USER DECimal Increases or decreases the level in steps of ten. USER Increases or decreases the level in increments, set with the command method RsSmbv.Source.Frequency.Step.increment.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FreqStepMode)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:STEP:MODE {param}')

	def get_increment(self) -> float:
		"""[SOURce<HW>]:FREQuency:STEP:[INCRement] \n
		Sets the step width. You can use this value to vary the RF frequency with command FREQ UP or FREQ DOWN, if you have
		activated FREQ:STEP:MODE USER. Note: This value also applies to the step width of the rotary knob on the instrument and,
		in user-defined step mode, increases or decreases the frequency. \n
			:return: increment: float Range: 0 Hz to RFmax - 100 kHz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:STEP:INCRement?')
		return Conversions.str_to_float(response)

	def set_increment(self, increment: float) -> None:
		"""[SOURce<HW>]:FREQuency:STEP:[INCRement] \n
		Sets the step width. You can use this value to vary the RF frequency with command FREQ UP or FREQ DOWN, if you have
		activated FREQ:STEP:MODE USER. Note: This value also applies to the step width of the rotary knob on the instrument and,
		in user-defined step mode, increases or decreases the frequency. \n
			:param increment: float Range: 0 Hz to RFmax - 100 kHz
		"""
		param = Conversions.decimal_value_to_str(increment)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:STEP:INCRement {param}')
