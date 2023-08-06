from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fixed:
	"""Fixed commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fixed", core, parent)

	# noinspection PyTypeChecker
	def get_recall(self) -> enums.InclExcl:
		"""[SOURce<HW>]:FREQuency:[FIXed]:RCL \n
		Set whether the RF frequency value is retained or taken from a loaded instrument configuration, when you recall
		instrument settings with command *RCL. \n
			:return: rcl: INCLude| EXCLude INCLude Takes the frequency value of the loaded settings. EXCLude Retains the current frequency when an instrument configuration is loaded.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:FIXed:RCL?')
		return Conversions.str_to_scalar_enum(response, enums.InclExcl)

	def set_recall(self, rcl: enums.InclExcl) -> None:
		"""[SOURce<HW>]:FREQuency:[FIXed]:RCL \n
		Set whether the RF frequency value is retained or taken from a loaded instrument configuration, when you recall
		instrument settings with command *RCL. \n
			:param rcl: INCLude| EXCLude INCLude Takes the frequency value of the loaded settings. EXCLude Retains the current frequency when an instrument configuration is loaded.
		"""
		param = Conversions.enum_scalar_to_str(rcl, enums.InclExcl)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:FIXed:RCL {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:FREQuency:[FIXed] \n
		Sets the frequency of the RF output signal in the selected path.
			INTRO_CMD_HELP: The effect depends on the selected mode: \n
			- In CW mode (FREQ:MODE CW | FIXed) , the instrument operates at a fixed frequency.
			- In sweep mode (FREQ:MODE SWE) , the value applies to the sweep frequency. The instrument processes the frequency settings in defined sweep steps.
			- In user mode (FREQ:STEP:MODE USER) , you can vary the current frequency step by step. \n
			:return: fixed: float The following settings influence the value range: An offset set with the command method RsSmbv.Source.Frequency.offset Numerical value Sets the frequency in CW and sweep mode UP|DOWN Varies the frequency step by step in user mode. The frequency is increased or decreased by the value set with the command method RsSmbv.Source.Frequency.Cw.value. Range: (RFmin + OFFSet) to (RFmax + OFFSet)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:FIXed?')
		return Conversions.str_to_float(response)

	def set_value(self, fixed: float) -> None:
		"""[SOURce<HW>]:FREQuency:[FIXed] \n
		Sets the frequency of the RF output signal in the selected path.
			INTRO_CMD_HELP: The effect depends on the selected mode: \n
			- In CW mode (FREQ:MODE CW | FIXed) , the instrument operates at a fixed frequency.
			- In sweep mode (FREQ:MODE SWE) , the value applies to the sweep frequency. The instrument processes the frequency settings in defined sweep steps.
			- In user mode (FREQ:STEP:MODE USER) , you can vary the current frequency step by step. \n
			:param fixed: float The following settings influence the value range: An offset set with the command method RsSmbv.Source.Frequency.offset Numerical value Sets the frequency in CW and sweep mode UP|DOWN Varies the frequency step by step in user mode. The frequency is increased or decreased by the value set with the command method RsSmbv.Source.Frequency.Cw.value. Range: (RFmin + OFFSet) to (RFmax + OFFSet)
		"""
		param = Conversions.decimal_value_to_str(fixed)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:FIXed {param}')
