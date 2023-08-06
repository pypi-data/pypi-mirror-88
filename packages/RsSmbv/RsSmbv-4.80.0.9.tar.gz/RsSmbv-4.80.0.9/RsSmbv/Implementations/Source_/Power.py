from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 35 total commands, 8 Sub-groups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def alc(self):
		"""alc commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_alc'):
			from .Power_.Alc import Alc
			self._alc = Alc(self._core, self._base)
		return self._alc

	@property
	def attenuation(self):
		"""attenuation commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_attenuation'):
			from .Power_.Attenuation import Attenuation
			self._attenuation = Attenuation(self._core, self._base)
		return self._attenuation

	@property
	def emf(self):
		"""emf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_emf'):
			from .Power_.Emf import Emf
			self._emf = Emf(self._core, self._base)
		return self._emf

	@property
	def limit(self):
		"""limit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_limit'):
			from .Power_.Limit import Limit
			self._limit = Limit(self._core, self._base)
		return self._limit

	@property
	def range(self):
		"""range commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_range'):
			from .Power_.Range import Range
			self._range = Range(self._core, self._base)
		return self._range

	@property
	def spc(self):
		"""spc commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_spc'):
			from .Power_.Spc import Spc
			self._spc = Spc(self._core, self._base)
		return self._spc

	@property
	def step(self):
		"""step commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_step'):
			from .Power_.Step import Step
			self._step = Step(self._core, self._base)
		return self._step

	@property
	def level(self):
		"""level commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Power_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	def get_iq_pep(self) -> float:
		"""[SOURce<HW>]:POWer:IQPep \n
		No command help available \n
			:return: ipart_qpep: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:IQPep?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_lbehaviour(self) -> enums.PowLevBehaviour:
		"""[SOURce<HW>]:POWer:LBEHaviour \n
		Selects the level behavior at the RF output over time. \n
			:return: behaviour: AUTO| UNINterrupted| MONotone| CVSWr| USER| CPHase UNINterrupted|MONotone Do not use the uninterrupted level settings and strictly monotone modes in combination with the high-quality optimization mode (see method RsSmbv.Source.Bb.Impairment.Optimization.mode) . CWSWr Constant VSWR
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:LBEHaviour?')
		return Conversions.str_to_scalar_enum(response, enums.PowLevBehaviour)

	def set_lbehaviour(self, behaviour: enums.PowLevBehaviour) -> None:
		"""[SOURce<HW>]:POWer:LBEHaviour \n
		Selects the level behavior at the RF output over time. \n
			:param behaviour: AUTO| UNINterrupted| MONotone| CVSWr| USER| CPHase UNINterrupted|MONotone Do not use the uninterrupted level settings and strictly monotone modes in combination with the high-quality optimization mode (see method RsSmbv.Source.Bb.Impairment.Optimization.mode) . CWSWr Constant VSWR
		"""
		param = Conversions.enum_scalar_to_str(behaviour, enums.PowLevBehaviour)
		self._core.io.write(f'SOURce<HwInstance>:POWer:LBEHaviour {param}')

	# noinspection PyTypeChecker
	def get_lmode(self) -> enums.PowLevMode:
		"""[SOURce<HW>]:POWer:LMODe \n
		No command help available \n
			:return: lev_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:LMODe?')
		return Conversions.str_to_scalar_enum(response, enums.PowLevMode)

	def set_lmode(self, lev_mode: enums.PowLevMode) -> None:
		"""[SOURce<HW>]:POWer:LMODe \n
		No command help available \n
			:param lev_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(lev_mode, enums.PowLevMode)
		self._core.io.write(f'SOURce<HwInstance>:POWer:LMODe {param}')

	def get_manual(self) -> float:
		"""[SOURce<HW>]:POWer:MANual \n
		Sets the level for the subsequent sweep step if method RsSmbv.Source.Sweep.Power.Mode.value. Use a separate command for
		each sweep step. \n
			:return: manual: float You can select any level within the setting range, where: STARt is set with method RsSmbv.Source.Power.start STOP is set with method RsSmbv.Source.Power.stop OFFSet is set with OFFSet Range: (STARt + OFFSet) to (STOP + OFFSet) , Unit: dBm
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:MANual?')
		return Conversions.str_to_float(response)

	def set_manual(self, manual: float) -> None:
		"""[SOURce<HW>]:POWer:MANual \n
		Sets the level for the subsequent sweep step if method RsSmbv.Source.Sweep.Power.Mode.value. Use a separate command for
		each sweep step. \n
			:param manual: float You can select any level within the setting range, where: STARt is set with method RsSmbv.Source.Power.start STOP is set with method RsSmbv.Source.Power.stop OFFSet is set with OFFSet Range: (STARt + OFFSet) to (STOP + OFFSet) , Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(manual)
		self._core.io.write(f'SOURce<HwInstance>:POWer:MANual {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.LfFreqMode:
		"""[SOURce<HW>]:POWer:MODE \n
		Selects the operating mode of the instrument to set the output level. \n
			:return: mode: CW| FIXed| SWEep CW|FIXed Operates at a constant level. CW and FIXed are synonyms. To set the output level value, use the command [:​SOURcehw]:​POWer[:​LEVel][:​IMMediate][:​AMPLitude]. SWEep Sets sweep mode. Set the range and current level with the commands: method RsSmbv.Source.Power.start and method RsSmbv.Source.Power.stop, method RsSmbv.Source.Power.manual.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.LfFreqMode)

	def set_mode(self, mode: enums.LfFreqMode) -> None:
		"""[SOURce<HW>]:POWer:MODE \n
		Selects the operating mode of the instrument to set the output level. \n
			:param mode: CW| FIXed| SWEep CW|FIXed Operates at a constant level. CW and FIXed are synonyms. To set the output level value, use the command [:​SOURcehw]:​POWer[:​LEVel][:​IMMediate][:​AMPLitude]. SWEep Sets sweep mode. Set the range and current level with the commands: method RsSmbv.Source.Power.start and method RsSmbv.Source.Power.stop, method RsSmbv.Source.Power.manual.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.LfFreqMode)
		self._core.io.write(f'SOURce<HwInstance>:POWer:MODE {param}')

	def get_pep(self) -> float:
		"""[SOURce<HW>]:POWer:PEP \n
		Queries the PEP 'Peak Envelope Power) of digital modulation or digital standards at the RF output. This value corresponds
		to the level specification, displayed in the status bar (header) . \n
			:return: pep: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:PEP?')
		return Conversions.str_to_float(response)

	def get_power(self) -> float:
		"""[SOURce<HW>]:POWer:POWer \n
		Sets the level at the RF output connector. This value does not consider a specified offset.
		The command [:​SOURce<hw>]:​POWer[:​LEVel][:​IMMediate][:​AMPLitude] sets the level of the 'Level' display, that means
		the level containing offset. See 'RF frequency and level display with a downstream instrument'. \n
			:return: power: float Level at the RF output, without level offset Range: See data sheet , Unit: dBm
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:POWer?')
		return Conversions.str_to_float(response)

	def set_power(self, power: float) -> None:
		"""[SOURce<HW>]:POWer:POWer \n
		Sets the level at the RF output connector. This value does not consider a specified offset.
		The command [:​SOURce<hw>]:​POWer[:​LEVel][:​IMMediate][:​AMPLitude] sets the level of the 'Level' display, that means
		the level containing offset. See 'RF frequency and level display with a downstream instrument'. \n
			:param power: float Level at the RF output, without level offset Range: See data sheet , Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(power)
		self._core.io.write(f'SOURce<HwInstance>:POWer:POWer {param}')

	def get_start(self) -> float:
		"""[SOURce<HW>]:POWer:STARt \n
		Sets the RF start/stop level in sweep mode. \n
			:return: start: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, start: float) -> None:
		"""[SOURce<HW>]:POWer:STARt \n
		Sets the RF start/stop level in sweep mode. \n
			:param start: float Sets the setting range calculated as follows: (Level_min + OFFSet) to (Level_max + OFFSet) Where the values are set with the commands: OFFSet method RsSmbv.Source.Power.start method RsSmbv.Source.Power.stop Range: Minimum level to maximum level , Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(start)
		self._core.io.write(f'SOURce<HwInstance>:POWer:STARt {param}')

	def get_stop(self) -> float:
		"""[SOURce<HW>]:POWer:STOP \n
		Sets the RF start/stop level in sweep mode. \n
			:return: stop: float Sets the setting range calculated as follows: (Level_min + OFFSet) to (Level_max + OFFSet) Where the values are set with the commands: OFFSet method RsSmbv.Source.Power.start method RsSmbv.Source.Power.stop Range: Minimum level to maximum level , Unit: dBm
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:STOP?')
		return Conversions.str_to_float(response)

	def set_stop(self, stop: float) -> None:
		"""[SOURce<HW>]:POWer:STOP \n
		Sets the RF start/stop level in sweep mode. \n
			:param stop: float Sets the setting range calculated as follows: (Level_min + OFFSet) to (Level_max + OFFSet) Where the values are set with the commands: OFFSet method RsSmbv.Source.Power.start method RsSmbv.Source.Power.stop Range: Minimum level to maximum level , Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(stop)
		self._core.io.write(f'SOURce<HwInstance>:POWer:STOP {param}')

	def get_wignore(self) -> bool:
		"""[SOURce]:POWer:WIGNore \n
		Ignores level range warnings. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce:POWer:WIGNore?')
		return Conversions.str_to_bool(response)

	def set_wignore(self, state: bool) -> None:
		"""[SOURce]:POWer:WIGNore \n
		Ignores level range warnings. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce:POWer:WIGNore {param}')
