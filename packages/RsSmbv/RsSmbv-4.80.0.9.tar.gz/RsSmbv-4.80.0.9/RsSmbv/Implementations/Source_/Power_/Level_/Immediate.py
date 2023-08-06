from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Immediate:
	"""Immediate commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("immediate", core, parent)

	def get_offset(self) -> float:
		"""[SOURce<HW>]:POWer:[LEVel]:[IMMediate]:OFFSet \n
		Sets the level offset of a downstream instrument. The level at the RF output is not changed. To query the resulting level,
		as it is at the output of the downstream instrument,
		use the command [:​SOURce<hw>]:​POWer[:​LEVel][:​IMMediate][:​AMPLitude]. See 'RF frequency and level display with a
		downstream instrument'. Note: The level offset also affects the RF level sweep. \n
			:return: offset: float Range: -200 to 200 , Unit: dB Level offset is always expreced in dB; linear units (V, W, etc.) are not supported
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:LEVel:IMMediate:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""[SOURce<HW>]:POWer:[LEVel]:[IMMediate]:OFFSet \n
		Sets the level offset of a downstream instrument. The level at the RF output is not changed. To query the resulting level,
		as it is at the output of the downstream instrument,
		use the command [:​SOURce<hw>]:​POWer[:​LEVel][:​IMMediate][:​AMPLitude]. See 'RF frequency and level display with a
		downstream instrument'. Note: The level offset also affects the RF level sweep. \n
			:param offset: float Range: -200 to 200 , Unit: dB Level offset is always expreced in dB; linear units (V, W, etc.) are not supported
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:POWer:LEVel:IMMediate:OFFSet {param}')

	# noinspection PyTypeChecker
	def get_recall(self) -> enums.InclExcl:
		"""[SOURce<HW>]:POWer:[LEVel]:[IMMediate]:RCL \n
		Determines whether the current level is retained or if the stored level setting is adopted when an instrument
		configuration is loaded. \n
			:return: rcl: INCLude| EXCLude INCLude Takes the current level when an instrument configuration is loaded. EXCLude Retains the current level when an instrument configuration is loaded.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:LEVel:IMMediate:RCL?')
		return Conversions.str_to_scalar_enum(response, enums.InclExcl)

	def set_recall(self, rcl: enums.InclExcl) -> None:
		"""[SOURce<HW>]:POWer:[LEVel]:[IMMediate]:RCL \n
		Determines whether the current level is retained or if the stored level setting is adopted when an instrument
		configuration is loaded. \n
			:param rcl: INCLude| EXCLude INCLude Takes the current level when an instrument configuration is loaded. EXCLude Retains the current level when an instrument configuration is loaded.
		"""
		param = Conversions.enum_scalar_to_str(rcl, enums.InclExcl)
		self._core.io.write(f'SOURce<HwInstance>:POWer:LEVel:IMMediate:RCL {param}')

	def get_amplitude(self) -> float:
		"""[SOURce<HW>]:POWer:[LEVel]:[IMMediate]:[AMPLitude] \n
		Sets the RF level applied to the DUT. To activate the RF output use command :​OUTPut<hw>[:​STATe] ('RF On'/'RF Off') .
			INTRO_CMD_HELP: The following applies POWer = RF output level + OFFSet, where: \n
			- method RsSmbv.Source.Power.Level.Immediate.amplitude is the values set with [:​SOURce<hw>]:​POWer[:​LEVel][:​IMMediate][:​AMPLitude]
			- RF output level is set with method RsSmbv.Source.Power.power
			- OFFSet is set with OFFSet \n
			:return: amplitude: float The following settings influence the value range: OFFSet set with the command OFFSet Numerical value Sets the level UP|DOWN Varies the level step by step. The level is increased or decreased by the value set with the command method RsSmbv.Source.Power.Level.Immediate.amplitude. Range: (Level_min + OFFSet) to (Level_max + OFFStet) , Unit: dBm
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:LEVel:IMMediate:AMPLitude?')
		return Conversions.str_to_float(response)

	def set_amplitude(self, amplitude: float) -> None:
		"""[SOURce<HW>]:POWer:[LEVel]:[IMMediate]:[AMPLitude] \n
		Sets the RF level applied to the DUT. To activate the RF output use command :​OUTPut<hw>[:​STATe] ('RF On'/'RF Off') .
			INTRO_CMD_HELP: The following applies POWer = RF output level + OFFSet, where: \n
			- method RsSmbv.Source.Power.Level.Immediate.amplitude is the values set with [:​SOURce<hw>]:​POWer[:​LEVel][:​IMMediate][:​AMPLitude]
			- RF output level is set with method RsSmbv.Source.Power.power
			- OFFSet is set with OFFSet \n
			:param amplitude: float The following settings influence the value range: OFFSet set with the command OFFSet Numerical value Sets the level UP|DOWN Varies the level step by step. The level is increased or decreased by the value set with the command method RsSmbv.Source.Power.Level.Immediate.amplitude. Range: (Level_min + OFFSet) to (Level_max + OFFStet) , Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(amplitude)
		self._core.io.write(f'SOURce<HwInstance>:POWer:LEVel:IMMediate:AMPLitude {param}')
