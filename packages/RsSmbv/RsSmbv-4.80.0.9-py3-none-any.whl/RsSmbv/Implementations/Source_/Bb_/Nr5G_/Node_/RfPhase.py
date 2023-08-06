from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfPhase:
	"""RfPhase commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rfPhase", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PcmOdeAll:
		"""[SOURce<HW>]:BB:NR5G:NODE:RFPHase:MODE \n
		Enables the frequency-related phase compensation after each symbol, as specified in . It uses the parameter 'Frequency in
		GHz' to set the carrier frequency to be compensated. \n
			:return: rf_phase_comp: 0| OFF| MANual| 1| AUTO 0|OFF Disables the frequency-related phase compensation. MANual Enables the 'Frequency in GHz' field for manual input of the carrier frequency value to be compensated. 1|AUTO Sets automatically the carrier 'Frequency in GHz' value to be compensated.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:NODE:RFPHase:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PcmOdeAll)

	def set_mode(self, rf_phase_comp: enums.PcmOdeAll) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:RFPHase:MODE \n
		Enables the frequency-related phase compensation after each symbol, as specified in . It uses the parameter 'Frequency in
		GHz' to set the carrier frequency to be compensated. \n
			:param rf_phase_comp: 0| OFF| MANual| 1| AUTO 0|OFF Disables the frequency-related phase compensation. MANual Enables the 'Frequency in GHz' field for manual input of the carrier frequency value to be compensated. 1|AUTO Sets automatically the carrier 'Frequency in GHz' value to be compensated.
		"""
		param = Conversions.enum_scalar_to_str(rf_phase_comp, enums.PcmOdeAll)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:RFPHase:MODE {param}')
