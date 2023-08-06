from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	# noinspection PyTypeChecker
	def get_advanced(self) -> enums.AutoManualMode:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:MODE:ADVanced \n
		No command help available \n
			:return: lf_sweep_mode_adv: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFOutput:SWEep:FREQuency:MODE:ADVanced?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)

	def set_advanced(self, lf_sweep_mode_adv: enums.AutoManualMode) -> None:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:MODE:ADVanced \n
		No command help available \n
			:param lf_sweep_mode_adv: No help available
		"""
		param = Conversions.enum_scalar_to_str(lf_sweep_mode_adv, enums.AutoManualMode)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput:SWEep:FREQuency:MODE:ADVanced {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.AutoManStep:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:MODE \n
		Sets the cycle mode of the LF sweep. \n
			:return: mode: AUTO| MANual| STEP AUTO Performs a complete sweep cycle from the start to the end value when a trigger event occurs. The dwell time determines the time period until the signal switches to the next step. MANual Performs a single sweep step when a manual trigger event occurs. The trigger system is not active. To trigger each frequency step of the sweep individually, use the command method RsSmbv.Source.LfOutput.Frequency.manual. STEP Each trigger command triggers one sweep step only. The frequency increases by the value set with the coammnds: method RsSmbv.Source.LfOutput.State.set (linear spacing) LFOutput:STEP:LOGarithmic(logarithmic spacing)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LFOutput:SWEep:FREQuency:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManStep)

	def set_value(self, mode: enums.AutoManStep) -> None:
		"""[SOURce<HW>]:LFOutput:SWEep:[FREQuency]:MODE \n
		Sets the cycle mode of the LF sweep. \n
			:param mode: AUTO| MANual| STEP AUTO Performs a complete sweep cycle from the start to the end value when a trigger event occurs. The dwell time determines the time period until the signal switches to the next step. MANual Performs a single sweep step when a manual trigger event occurs. The trigger system is not active. To trigger each frequency step of the sweep individually, use the command method RsSmbv.Source.LfOutput.Frequency.manual. STEP Each trigger command triggers one sweep step only. The frequency increases by the value set with the coammnds: method RsSmbv.Source.LfOutput.State.set (linear spacing) LFOutput:STEP:LOGarithmic(logarithmic spacing)
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AutoManStep)
		self._core.io.write(f'SOURce<HwInstance>:LFOutput:SWEep:FREQuency:MODE {param}')
