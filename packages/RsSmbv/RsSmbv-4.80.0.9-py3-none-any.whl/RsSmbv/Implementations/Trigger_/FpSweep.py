from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FpSweep:
	"""FpSweep commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fpSweep", core, parent)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.SingExtAuto:
		"""TRIGger<HW>:FPSWeep:SOURce \n
		Selects the trigger source for the combined RF frequency / level sweep. The parameter names correspond to the manual
		control. If needed, see table Table 'Cross-reference between the manual and remote control ' for selecting the trigger
		source with SCPI compliant parameter names. \n
			:return: fp_trig_source: AUTO| IMMediate | SINGle| BUS| EXTernal | EAUTo AUTO|IMMediate Executes the combined RF sweep automatically. In this free-running mode, the trigger condition is met continuously. I.e. as soon as a sweep is completed, the next one starts immediately. SINGle|BUS Executes one complete sweep cycle triggered by the GPIB commands method RsSmbv.Source.Sweep.Combined.Execute.set or *TRG. The mode has to be set to [:SOURcehw]:SWEep:COMBined:MODE AUTO. EXTernal An external signal triggers the sweep. EAUTo An external signal triggers the sweep. As soon as one sweep is finished, the next sweep starts. A second trigger event stops the sweep at the current frequency and level value pairs, a third trigger event starts the trigger at the start values, and so on.
		"""
		response = self._core.io.query_str('TRIGger<HwInstance>:FPSWeep:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SingExtAuto)

	def set_source(self, fp_trig_source: enums.SingExtAuto) -> None:
		"""TRIGger<HW>:FPSWeep:SOURce \n
		Selects the trigger source for the combined RF frequency / level sweep. The parameter names correspond to the manual
		control. If needed, see table Table 'Cross-reference between the manual and remote control ' for selecting the trigger
		source with SCPI compliant parameter names. \n
			:param fp_trig_source: AUTO| IMMediate | SINGle| BUS| EXTernal | EAUTo AUTO|IMMediate Executes the combined RF sweep automatically. In this free-running mode, the trigger condition is met continuously. I.e. as soon as a sweep is completed, the next one starts immediately. SINGle|BUS Executes one complete sweep cycle triggered by the GPIB commands method RsSmbv.Source.Sweep.Combined.Execute.set or *TRG. The mode has to be set to [:SOURcehw]:SWEep:COMBined:MODE AUTO. EXTernal An external signal triggers the sweep. EAUTo An external signal triggers the sweep. As soon as one sweep is finished, the next sweep starts. A second trigger event stops the sweep at the current frequency and level value pairs, a third trigger event starts the trigger at the start values, and so on.
		"""
		param = Conversions.enum_scalar_to_str(fp_trig_source, enums.SingExtAuto)
		self._core.io.write(f'TRIGger<HwInstance>:FPSWeep:SOURce {param}')
