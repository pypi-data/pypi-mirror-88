from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	# noinspection PyTypeChecker
	def get_advanced(self) -> enums.AutoManualMode:
		"""[SOURce<HW>]:SWEep:POWer:MODE:ADVanced \n
		No command help available \n
			:return: pow_mode_adv: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:MODE:ADVanced?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)

	def set_advanced(self, pow_mode_adv: enums.AutoManualMode) -> None:
		"""[SOURce<HW>]:SWEep:POWer:MODE:ADVanced \n
		No command help available \n
			:param pow_mode_adv: No help available
		"""
		param = Conversions.enum_scalar_to_str(pow_mode_adv, enums.AutoManualMode)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:MODE:ADVanced {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.AutoManStep:
		"""[SOURce<HW>]:SWEep:POWer:MODE \n
		Sets the cycle mode for the level sweep. \n
			:return: mode: AUTO| MANual| STEP AUTO Each trigger triggers exactly one complete sweep. MANual The trigger system is not active. You can trigger every step individually with the command method RsSmbv.Source.Power.manual. The level value increases at each step by the value that you define with method RsSmbv.Source.Power.Level.Immediate.amplitude. Values directly entered with the command method RsSmbv.Source.Power.manual are not taken into account. STEP Each trigger triggers one sweep step only. The level increases by the value entered with method RsSmbv.Source.Power.Level.Immediate.amplitude.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:SWEep:POWer:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManStep)

	def set_value(self, mode: enums.AutoManStep) -> None:
		"""[SOURce<HW>]:SWEep:POWer:MODE \n
		Sets the cycle mode for the level sweep. \n
			:param mode: AUTO| MANual| STEP AUTO Each trigger triggers exactly one complete sweep. MANual The trigger system is not active. You can trigger every step individually with the command method RsSmbv.Source.Power.manual. The level value increases at each step by the value that you define with method RsSmbv.Source.Power.Level.Immediate.amplitude. Values directly entered with the command method RsSmbv.Source.Power.manual are not taken into account. STEP Each trigger triggers one sweep step only. The level increases by the value entered with method RsSmbv.Source.Power.Level.Immediate.amplitude.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AutoManStep)
		self._core.io.write(f'SOURce<HwInstance>:SWEep:POWer:MODE {param}')
