from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	# noinspection PyTypeChecker
	def get_advanced(self) -> enums.AutoManualMode:
		"""[SOURce<HW>]:LIST:MODE:ADVanced \n
		No command help available \n
			:return: list_mode_adv: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:MODE:ADVanced?')
		return Conversions.str_to_scalar_enum(response, enums.AutoManualMode)

	def set_advanced(self, list_mode_adv: enums.AutoManualMode) -> None:
		"""[SOURce<HW>]:LIST:MODE:ADVanced \n
		No command help available \n
			:param list_mode_adv: No help available
		"""
		param = Conversions.enum_scalar_to_str(list_mode_adv, enums.AutoManualMode)
		self._core.io.write(f'SOURce<HwInstance>:LIST:MODE:ADVanced {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.AutoStep:
		"""[SOURce<HW>]:LIST:MODE \n
		Sets the list mode. The instrument processes the list according to the selected mode and trigger source.
		See LIST:TRIG:SOUR AUTO, SING or EXT for the description of the trigger source settings. \n
			:return: mode: AUTO| STEP AUTO Each trigger event triggers a complete list cycle. STEP Each trigger event triggers only one step in the list processing cycle. The list is processed in ascending order.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AutoStep)

	def set_value(self, mode: enums.AutoStep) -> None:
		"""[SOURce<HW>]:LIST:MODE \n
		Sets the list mode. The instrument processes the list according to the selected mode and trigger source.
		See LIST:TRIG:SOUR AUTO, SING or EXT for the description of the trigger source settings. \n
			:param mode: AUTO| STEP AUTO Each trigger event triggers a complete list cycle. STEP Each trigger event triggers only one step in the list processing cycle. The list is processed in ascending order.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AutoStep)
		self._core.io.write(f'SOURce<HwInstance>:LIST:MODE {param}')
