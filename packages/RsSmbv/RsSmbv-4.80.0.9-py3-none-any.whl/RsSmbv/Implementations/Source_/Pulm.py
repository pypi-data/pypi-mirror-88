from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pulm:
	"""Pulm commands group definition. 15 total commands, 3 Sub-groups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pulm", core, parent)

	def clone(self) -> 'Pulm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pulm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def double(self):
		"""double commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_double'):
			from .Pulm_.Double import Double
			self._double = Double(self._core, self._base)
		return self._double

	@property
	def trigger(self):
		"""trigger commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Pulm_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def internal(self):
		"""internal commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_internal'):
			from .Pulm_.Internal import Internal
			self._internal = Internal(self._core, self._base)
		return self._internal

	def get_delay(self) -> float:
		"""[SOURce<HW>]:PULM:DELay \n
		Sets the pulse delay. \n
			:return: delay: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""[SOURce<HW>]:PULM:DELay \n
		Sets the pulse delay. \n
			:param delay: float
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:PULM:DELay {param}')

	# noinspection PyTypeChecker
	def get_impedance(self) -> enums.InputImpRf:
		"""[SOURce<HW>]:PULM:IMPedance \n
		Sets the impedance for the external pulse trigger and pulse modulation input. \n
			:return: impedance: G50| G10K
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.InputImpRf)

	def set_impedance(self, impedance: enums.InputImpRf) -> None:
		"""[SOURce<HW>]:PULM:IMPedance \n
		Sets the impedance for the external pulse trigger and pulse modulation input. \n
			:param impedance: G50| G10K
		"""
		param = Conversions.enum_scalar_to_str(impedance, enums.InputImpRf)
		self._core.io.write(f'SOURce<HwInstance>:PULM:IMPedance {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PulsMode:
		"""[SOURce<HW>]:PULM:MODE \n
		Selects the mode for the pulse modulation. \n
			:return: mode: SINGle| DOUBle SINGle Generates a single pulse. DOUBle Generates two pulses within one pulse period.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PulsMode)

	def set_mode(self, mode: enums.PulsMode) -> None:
		"""[SOURce<HW>]:PULM:MODE \n
		Selects the mode for the pulse modulation. \n
			:param mode: SINGle| DOUBle SINGle Generates a single pulse. DOUBle Generates two pulses within one pulse period.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.PulsMode)
		self._core.io.write(f'SOURce<HwInstance>:PULM:MODE {param}')

	def get_period(self) -> float:
		"""[SOURce<HW>]:PULM:PERiod \n
		Sets the period of the generated pulse, that means the repetition frequency of the internally generated modulation signal. \n
			:return: period: float The minimum value depends on the installed options R&S SMBVB-K22 or R&S SMBVB-K23 Range: 20E-9 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:PERiod?')
		return Conversions.str_to_float(response)

	def set_period(self, period: float) -> None:
		"""[SOURce<HW>]:PULM:PERiod \n
		Sets the period of the generated pulse, that means the repetition frequency of the internally generated modulation signal. \n
			:param period: float The minimum value depends on the installed options R&S SMBVB-K22 or R&S SMBVB-K23 Range: 20E-9 to 100
		"""
		param = Conversions.decimal_value_to_str(period)
		self._core.io.write(f'SOURce<HwInstance>:PULM:PERiod {param}')

	# noinspection PyTypeChecker
	def get_polarity(self) -> enums.NormInv:
		"""[SOURce<HW>]:PULM:POLarity \n
		Sets the polarity of the externally applied modulation signal. \n
			:return: polarity: NORMal| INVerted NORMal Suppresses the RF signal during the pulse pause. INVerted Suppresses the RF signal during the pulse.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:POLarity?')
		return Conversions.str_to_scalar_enum(response, enums.NormInv)

	def set_polarity(self, polarity: enums.NormInv) -> None:
		"""[SOURce<HW>]:PULM:POLarity \n
		Sets the polarity of the externally applied modulation signal. \n
			:param polarity: NORMal| INVerted NORMal Suppresses the RF signal during the pulse pause. INVerted Suppresses the RF signal during the pulse.
		"""
		param = Conversions.enum_scalar_to_str(polarity, enums.NormInv)
		self._core.io.write(f'SOURce<HwInstance>:PULM:POLarity {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.SourceInt:
		"""[SOURce<HW>]:PULM:SOURce \n
		Selects between the internal (pulse generator) or an external pulse signal for the modulation. \n
			:return: source: INTernal| EXTernal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SourceInt)

	def set_source(self, source: enums.SourceInt) -> None:
		"""[SOURce<HW>]:PULM:SOURce \n
		Selects between the internal (pulse generator) or an external pulse signal for the modulation. \n
			:param source: INTernal| EXTernal
		"""
		param = Conversions.enum_scalar_to_str(source, enums.SourceInt)
		self._core.io.write(f'SOURce<HwInstance>:PULM:SOURce {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:PULM:STATe \n
		Activates pulse modulation. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:PULM:STATe \n
		Activates pulse modulation. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:PULM:STATe {param}')

	# noinspection PyTypeChecker
	def get_ttype(self) -> enums.PulsTransType:
		"""[SOURce<HW>]:PULM:TTYPe \n
		Sets the transition mode for the pulse signal. \n
			:return: source: SMOothed| FAST SMOothed flattens the slew rate, resulting in longer rise/fall times. FAST enables fast transitions with shortest rise and fall times.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:TTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.PulsTransType)

	def set_ttype(self, source: enums.PulsTransType) -> None:
		"""[SOURce<HW>]:PULM:TTYPe \n
		Sets the transition mode for the pulse signal. \n
			:param source: SMOothed| FAST SMOothed flattens the slew rate, resulting in longer rise/fall times. FAST enables fast transitions with shortest rise and fall times.
		"""
		param = Conversions.enum_scalar_to_str(source, enums.PulsTransType)
		self._core.io.write(f'SOURce<HwInstance>:PULM:TTYPe {param}')

	def get_width(self) -> float:
		"""[SOURce<HW>]:PULM:WIDTh \n
		Sets the width of the generated pulse, that means the pulse length. It must be at least 20ns less than the set pulse
		period. \n
			:return: width: float Range: 20E-9 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PULM:WIDTh?')
		return Conversions.str_to_float(response)

	def set_width(self, width: float) -> None:
		"""[SOURce<HW>]:PULM:WIDTh \n
		Sets the width of the generated pulse, that means the pulse length. It must be at least 20ns less than the set pulse
		period. \n
			:param width: float Range: 20E-9 to 100
		"""
		param = Conversions.decimal_value_to_str(width)
		self._core.io.write(f'SOURce<HwInstance>:PULM:WIDTh {param}')
