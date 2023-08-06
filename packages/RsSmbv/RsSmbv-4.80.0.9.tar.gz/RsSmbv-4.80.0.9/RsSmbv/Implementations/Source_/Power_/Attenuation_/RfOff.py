from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfOff:
	"""RfOff commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rfOff", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PowAttRfOffMode:
		"""[SOURce<HW>]:POWer:ATTenuation:RFOFf:MODE \n
		Selects the state the attenuator is to assume if the RF signal is switched off. \n
			:return: mode: UNCHanged| FATTenuation FATTenuation The step attenuator switches to maximum attenuation UNCHanged Retains the current setting and keeps the output impedance constant during RF off.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:POWer:ATTenuation:RFOFf:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PowAttRfOffMode)

	def set_mode(self, mode: enums.PowAttRfOffMode) -> None:
		"""[SOURce<HW>]:POWer:ATTenuation:RFOFf:MODE \n
		Selects the state the attenuator is to assume if the RF signal is switched off. \n
			:param mode: UNCHanged| FATTenuation FATTenuation The step attenuator switches to maximum attenuation UNCHanged Retains the current setting and keeps the output impedance constant during RF off.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.PowAttRfOffMode)
		self._core.io.write(f'SOURce<HwInstance>:POWer:ATTenuation:RFOFf:MODE {param}')
