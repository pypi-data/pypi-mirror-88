from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pinput:
	"""Pinput commands group definition. 4 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pinput", core, parent)

	def clone(self) -> 'Pinput':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pinput(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_trigger'):
			from .Pinput_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def get_delay(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:PINPut:DELay \n
		Sets the delay between the external trigger and the first DME output pulse (50% voltage point of first pulse) . Setting
		takes effect, if [:SOURce<hw>][:BB]:DME:PINPut:SOURce is set to EXTernal. For DME reply mode, this setting simulates the
		defined delay of the DME transponder and twice the run time of the signal (from interrogator to transponder and back) .
		The delay is a measure of the range distance, thus, the two values are interdependent according to: Delay = X/Y mode
		delay + range distance * 12.359 nm/μs (X mode delay = 50 μs, Y mode delay is 56 μs) Changing one value automatically
		changes the other value. \n
			:return: delay: float Range: 4E-6 to 5E-3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:PINPut:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""[SOURce<HW>]:[BB]:DME:PINPut:DELay \n
		Sets the delay between the external trigger and the first DME output pulse (50% voltage point of first pulse) . Setting
		takes effect, if [:SOURce<hw>][:BB]:DME:PINPut:SOURce is set to EXTernal. For DME reply mode, this setting simulates the
		defined delay of the DME transponder and twice the run time of the signal (from interrogator to transponder and back) .
		The delay is a measure of the range distance, thus, the two values are interdependent according to: Delay = X/Y mode
		delay + range distance * 12.359 nm/μs (X mode delay = 50 μs, Y mode delay is 56 μs) Changing one value automatically
		changes the other value. \n
			:param delay: float Range: 4E-6 to 5E-3
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:PINPut:DELay {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.AvionicDmePulsInput:
		"""[SOURce<HW>]:[BB]:DME:PINPut:SOURce \n
		Selects the trigger mode for DME modulation signals. \n
			:return: puls_inp_source: EXTernal| PSENsor EXTernal The signals are triggered by an external trigger event. The trigger signal is supplied via the Pulse Ext connector. PSENsor The signals are triggered by R&S NRP-Z81 power sensor. This mode requires, that [:SOURcehw][:BB]:DME:MODE is set to INTerrogation.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:PINPut:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicDmePulsInput)

	def set_source(self, puls_inp_source: enums.AvionicDmePulsInput) -> None:
		"""[SOURce<HW>]:[BB]:DME:PINPut:SOURce \n
		Selects the trigger mode for DME modulation signals. \n
			:param puls_inp_source: EXTernal| PSENsor EXTernal The signals are triggered by an external trigger event. The trigger signal is supplied via the Pulse Ext connector. PSENsor The signals are triggered by R&S NRP-Z81 power sensor. This mode requires, that [:SOURcehw][:BB]:DME:MODE is set to INTerrogation.
		"""
		param = Conversions.enum_scalar_to_str(puls_inp_source, enums.AvionicDmePulsInput)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:PINPut:SOURce {param}')
