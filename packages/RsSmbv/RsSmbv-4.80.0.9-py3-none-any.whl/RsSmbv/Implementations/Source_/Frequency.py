from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 19 total commands, 4 Sub-groups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def loscillator(self):
		"""loscillator commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_loscillator'):
			from .Frequency_.Loscillator import Loscillator
			self._loscillator = Loscillator(self._core, self._base)
		return self._loscillator

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_step'):
			from .Frequency_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	@property
	def cw(self):
		"""cw commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_cw'):
			from .Frequency_.Cw import Cw
			self._cw = Cw(self._core, self._base)
		return self._cw

	@property
	def fixed(self):
		"""fixed commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_fixed'):
			from .Frequency_.Fixed import Fixed
			self._fixed = Fixed(self._core, self._base)
		return self._fixed

	def get_center(self) -> float:
		"""[SOURce<HW>]:FREQuency:CENTer \n
		Sets the center frequency of the sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:return: center: float Range: 300 kHz to RFmax, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:CENTer?')
		return Conversions.str_to_float(response)

	def set_center(self, center: float) -> None:
		"""[SOURce<HW>]:FREQuency:CENTer \n
		Sets the center frequency of the sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:param center: float Range: 300 kHz to RFmax, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(center)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:CENTer {param}')

	def get_frequency(self) -> float:
		"""[SOURce<HW>]:FREQuency:FREQuency \n
		No command help available \n
			:return: frequency: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""[SOURce<HW>]:FREQuency:FREQuency \n
		No command help available \n
			:param frequency: No help available
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:FREQuency {param}')

	def get_manual(self) -> float:
		"""[SOURce<HW>]:FREQuency:MANual \n
		Sets the frequency and triggers a sweep step manually if SWEep:MODE MAN. \n
			:return: manual: float You can select any frequency within the setting range, where: STARt is set with method RsSmbv.Source.Frequency.start STOP is set with method RsSmbv.Source.Frequency.stop OFFSet is set with method RsSmbv.Source.Frequency.offset Range: (STARt + OFFSet) to (STOP + OFFSet) , Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MANual?')
		return Conversions.str_to_float(response)

	def set_manual(self, manual: float) -> None:
		"""[SOURce<HW>]:FREQuency:MANual \n
		Sets the frequency and triggers a sweep step manually if SWEep:MODE MAN. \n
			:param manual: float You can select any frequency within the setting range, where: STARt is set with method RsSmbv.Source.Frequency.start STOP is set with method RsSmbv.Source.Frequency.stop OFFSet is set with method RsSmbv.Source.Frequency.offset Range: (STARt + OFFSet) to (STOP + OFFSet) , Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(manual)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MANual {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FreqMode:
		"""[SOURce<HW>]:FREQuency:MODE \n
		Sets the frequency mode for generating the RF output signal. The selected mode determines the parameters to be used for
		further frequency settings. \n
			:return: mode: CW| FIXed | SWEep| LIST | COMBined CW|FIXed Sets the fixed frequency mode. CW and FIXed are synonyms. The instrument operates at a defined frequency, set with command [:​SOURcehw]:​FREQuency[:​CW|FIXed]. SWEep Sets sweep mode. The instrument processes frequency (and level) settings in defined sweep steps. Set the range and current frequency with the commands: method RsSmbv.Source.Frequency.start and method RsSmbv.Source.Frequency.stop, method RsSmbv.Source.Frequency.center, method RsSmbv.Source.Frequency.span, method RsSmbv.Source.Frequency.manual LIST Sets list mode. The instrument processes frequency and level settings by means of values loaded from a list. To configure list mode settings, use the commands of the 'SOURce:LIST Subsystem'. COMBined Sets the combined RF frequency / level sweep mode. The instrument processes frequency and level settings in defined sweep steps. Set the range and current frequency with the commands: method RsSmbv.Source.Combined.Frequency.start and method RsSmbv.Source.Combined.Frequency.stop, method RsSmbv.Source.Combined.Power.start and method RsSmbv.Source.Combined.Power.stop
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FreqMode)

	def set_mode(self, mode: enums.FreqMode) -> None:
		"""[SOURce<HW>]:FREQuency:MODE \n
		Sets the frequency mode for generating the RF output signal. The selected mode determines the parameters to be used for
		further frequency settings. \n
			:param mode: CW| FIXed | SWEep| LIST | COMBined CW|FIXed Sets the fixed frequency mode. CW and FIXed are synonyms. The instrument operates at a defined frequency, set with command [:​SOURcehw]:​FREQuency[:​CW|FIXed]. SWEep Sets sweep mode. The instrument processes frequency (and level) settings in defined sweep steps. Set the range and current frequency with the commands: method RsSmbv.Source.Frequency.start and method RsSmbv.Source.Frequency.stop, method RsSmbv.Source.Frequency.center, method RsSmbv.Source.Frequency.span, method RsSmbv.Source.Frequency.manual LIST Sets list mode. The instrument processes frequency and level settings by means of values loaded from a list. To configure list mode settings, use the commands of the 'SOURce:LIST Subsystem'. COMBined Sets the combined RF frequency / level sweep mode. The instrument processes frequency and level settings in defined sweep steps. Set the range and current frequency with the commands: method RsSmbv.Source.Combined.Frequency.start and method RsSmbv.Source.Combined.Frequency.stop, method RsSmbv.Source.Combined.Power.start and method RsSmbv.Source.Combined.Power.stop
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FreqMode)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MODE {param}')

	def get_multiplier(self) -> float:
		"""[SOURce<HW>]:FREQuency:MULTiplier \n
		Sets the multiplication factor NFREQ:MULT of a subsequent downstream instrument. The parameters offset fFREQ:OFFSer and
		multiplier NFREQ:MULT affect the frequency value set with the command [:​SOURce<hw>]:​FREQuency[:​CW|FIXed]. The query
		[:​SOURce<hw>]:​FREQuency[:​CW|FIXed] returns the value corresponding to the formula: fFREQ = fRFout * NFREQ:MULT +
		fFREQ:OFFSer See 'RF frequency and level display with a downstream instrument'. \n
			:return: multiplier: float Range: -10000 to 10000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:MULTiplier?')
		return Conversions.str_to_float(response)

	def set_multiplier(self, multiplier: float) -> None:
		"""[SOURce<HW>]:FREQuency:MULTiplier \n
		Sets the multiplication factor NFREQ:MULT of a subsequent downstream instrument. The parameters offset fFREQ:OFFSer and
		multiplier NFREQ:MULT affect the frequency value set with the command [:​SOURce<hw>]:​FREQuency[:​CW|FIXed]. The query
		[:​SOURce<hw>]:​FREQuency[:​CW|FIXed] returns the value corresponding to the formula: fFREQ = fRFout * NFREQ:MULT +
		fFREQ:OFFSer See 'RF frequency and level display with a downstream instrument'. \n
			:param multiplier: float Range: -10000 to 10000
		"""
		param = Conversions.decimal_value_to_str(multiplier)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:MULTiplier {param}')

	def get_offset(self) -> float:
		"""[SOURce<HW>]:FREQuency:OFFSet \n
		Sets the frequency offset fFREQ:OFFSet of a downstream instrument. The parameters offset fFREQ:OFFSer and multiplier
		NFREQ:MULT affect the frequency value set with the command [:​SOURce<hw>]:​FREQuency[:​CW|FIXed].
		The query [:​SOURce<hw>]:​FREQuency[:​CW|FIXed] returns the value corresponding to the formula: fFREQ = fRFout *
		NFREQ:MULT + fFREQ:OFFSer See 'RF frequency and level display with a downstream instrument'. Note: The offset also
		affects RF frequency sweep. \n
			:return: offset: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""[SOURce<HW>]:FREQuency:OFFSet \n
		Sets the frequency offset fFREQ:OFFSet of a downstream instrument. The parameters offset fFREQ:OFFSer and multiplier
		NFREQ:MULT affect the frequency value set with the command [:​SOURce<hw>]:​FREQuency[:​CW|FIXed].
		The query [:​SOURce<hw>]:​FREQuency[:​CW|FIXed] returns the value corresponding to the formula: fFREQ = fRFout *
		NFREQ:MULT + fFREQ:OFFSer See 'RF frequency and level display with a downstream instrument'. Note: The offset also
		affects RF frequency sweep. \n
			:param offset: float
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:OFFSet {param}')

	def get_span(self) -> float:
		"""[SOURce<HW>]:FREQuency:SPAN \n
		Sets the sapn of the frequency sweep range. See 'Correlating Parameters in Sweep Mode'. \n
			:return: span: float Full freqeuncy range
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:SPAN?')
		return Conversions.str_to_float(response)

	def set_span(self, span: float) -> None:
		"""[SOURce<HW>]:FREQuency:SPAN \n
		Sets the sapn of the frequency sweep range. See 'Correlating Parameters in Sweep Mode'. \n
			:param span: float Full freqeuncy range
		"""
		param = Conversions.decimal_value_to_str(span)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:SPAN {param}')

	def get_start(self) -> float:
		"""[SOURce<HW>]:FREQuency:STARt \n
		Sets the start frequency for the RF sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:return: start: float Range: 300kHz to RFmax
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, start: float) -> None:
		"""[SOURce<HW>]:FREQuency:STARt \n
		Sets the start frequency for the RF sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:param start: float Range: 300kHz to RFmax
		"""
		param = Conversions.decimal_value_to_str(start)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:STARt {param}')

	def get_stop(self) -> float:
		"""[SOURce<HW>]:FREQuency:STOP \n
		Sets the stop frequency range for the RF sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:return: stop: float Range: 300kHz to RFmax, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:STOP?')
		return Conversions.str_to_float(response)

	def set_stop(self, stop: float) -> None:
		"""[SOURce<HW>]:FREQuency:STOP \n
		Sets the stop frequency range for the RF sweep. See 'Correlating Parameters in Sweep Mode'. \n
			:param stop: float Range: 300kHz to RFmax, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(stop)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:STOP {param}')
