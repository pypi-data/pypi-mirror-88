from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Iq:
	"""Iq commands group definition. 180 total commands, 6 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iq", core, parent)

	def clone(self) -> 'Iq':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Iq(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def doherty(self):
		"""doherty commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_doherty'):
			from .Iq_.Doherty import Doherty
			self._doherty = Doherty(self._core, self._base)
		return self._doherty

	@property
	def dpd(self):
		"""dpd commands group. 13 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpd'):
			from .Iq_.Dpd import Dpd
			self._dpd = Dpd(self._core, self._base)
		return self._dpd

	@property
	def emixer(self):
		"""emixer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_emixer'):
			from .Iq_.Emixer import Emixer
			self._emixer = Emixer(self._core, self._base)
		return self._emixer

	@property
	def impairment(self):
		"""impairment commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_impairment'):
			from .Iq_.Impairment import Impairment
			self._impairment = Impairment(self._core, self._base)
		return self._impairment

	@property
	def output(self):
		"""output commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Iq_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	@property
	def swap(self):
		"""swap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swap'):
			from .Iq_.Swap import Swap
			self._swap = Swap(self._core, self._base)
		return self._swap

	def get_crest_factor(self) -> float:
		"""[SOURce<HW>]:IQ:CREStfactor \n
		Specifies the crest factor for the external analog signal. \n
			:return: crest_factor: float Range: 0 to 35, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:CREStfactor?')
		return Conversions.str_to_float(response)

	def set_crest_factor(self, crest_factor: float) -> None:
		"""[SOURce<HW>]:IQ:CREStfactor \n
		Specifies the crest factor for the external analog signal. \n
			:param crest_factor: float Range: 0 to 35, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(crest_factor)
		self._core.io.write(f'SOURce<HwInstance>:IQ:CREStfactor {param}')

	# noinspection PyTypeChecker
	def get_gain(self) -> enums.IqGain:
		"""[SOURce<HW>]:IQ:GAIN \n
		Optimizes the modulation of the I/Q modulator for a subset of measurement requirement. \n
			:return: gain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:GAIN?')
		return Conversions.str_to_scalar_enum(response, enums.IqGain)

	def set_gain(self, gain: enums.IqGain) -> None:
		"""[SOURce<HW>]:IQ:GAIN \n
		Optimizes the modulation of the I/Q modulator for a subset of measurement requirement. \n
			:param gain: DBM4| DBM2| DB0| DB2| DB4| DB8| DB6 Dynamic range of 16 dB divided into 2 dB steps. DB0|DB2|DB4|DB6|DB8 Activates the specified gain of 0 dB, +2 dB, +4 dB, +6 dB, +8 dB DBM2|DBM4 Activates the specified gain of -2 dB, -4 dB
		"""
		param = Conversions.enum_scalar_to_str(gain, enums.IqGain)
		self._core.io.write(f'SOURce<HwInstance>:IQ:GAIN {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.IqMode:
		"""[SOURce<HW>]:IQ:SOURce \n
		Selects the input signal source for the I/Q modulator. \n
			:return: source: BASeband| ANALog External signals disable the amplitude modulation, an enabled custom digital modulation, any configured digital standard or an applied digital baseband input signal.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.IqMode)

	def set_source(self, source: enums.IqMode) -> None:
		"""[SOURce<HW>]:IQ:SOURce \n
		Selects the input signal source for the I/Q modulator. \n
			:param source: BASeband| ANALog External signals disable the amplitude modulation, an enabled custom digital modulation, any configured digital standard or an applied digital baseband input signal.
		"""
		param = Conversions.enum_scalar_to_str(source, enums.IqMode)
		self._core.io.write(f'SOURce<HwInstance>:IQ:SOURce {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:IQ:STATe \n
		Enables/disables the I/Q modulation. Note: Interdependencies
			INTRO_CMD_HELP: The following functions cannot be activated simultaneously. They deactivate each other. \n
			- The internal baseband generator ([:SOURce<hw>]:BB:<DigStd>:STATe) and the external digital baseband input ([:SOURce<hw>]:BBIN:STATe)
			- The external digital baseband input ([:SOURce<hw>]:BBIN:STATe) and digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) because they share the same physical connectors (Dig I/Q and the HS Dig I/Q) .
			- The digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) and the output of analog I/Q signals:
			Table Header:  \n
			- If [:SOURce<hw>]:IQ:SOURce BASeband, [:SOURce<hw>]:IQ:STATe + method RsSmbv.Output.State.value or
			- [:SOURce<hw>]:IQ:OUTPut:ANALog:STATe \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:STATe?')
		return Conversions.str_to_bool(response)

	def get_wb_state(self) -> bool:
		"""[SOURce<HW>]:IQ:WBSTate \n
		Activates wideband mode. This setting automatically optimizes the settings for wideband modulation signals (>5 MHz, State
		ON) . \n
			:return: wb_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:WBSTate?')
		return Conversions.str_to_bool(response)

	def set_wb_state(self, wb_state: bool) -> None:
		"""[SOURce<HW>]:IQ:WBSTate \n
		Activates wideband mode. This setting automatically optimizes the settings for wideband modulation signals (>5 MHz, State
		ON) . \n
			:param wb_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(wb_state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:WBSTate {param}')
