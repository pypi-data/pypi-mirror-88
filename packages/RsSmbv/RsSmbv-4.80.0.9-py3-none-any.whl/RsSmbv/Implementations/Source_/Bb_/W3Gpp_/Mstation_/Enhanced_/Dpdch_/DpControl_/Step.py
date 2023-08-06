from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Step:
	"""Step commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("step", core, parent)

	# noinspection PyTypeChecker
	def get_manual(self) -> enums.PowContStepMan:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:STEP:MANual \n
		Sets the control signal for manual mode of Dynamic Power Control. \n
			:return: manual: MAN0| MAN1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:STEP:MANual?')
		return Conversions.str_to_scalar_enum(response, enums.PowContStepMan)

	def set_manual(self, manual: enums.PowContStepMan) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:STEP:MANual \n
		Sets the control signal for manual mode of Dynamic Power Control. \n
			:param manual: MAN0| MAN1
		"""
		param = Conversions.enum_scalar_to_str(manual, enums.PowContStepMan)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:STEP:MANual {param}')

	def get_external(self) -> float:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:STEP:[EXTernal] \n
		This command sets step width by which – with Dynamic Power Control being switched on - the channel power of the enhanced
		channels is increased or decreased. \n
			:return: external: float Range: 0.5 to 6, Unit: dB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:STEP:EXTernal?')
		return Conversions.str_to_float(response)

	def set_external(self, external: float) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:[ENHanced]:[DPDCh]:DPControl:STEP:[EXTernal] \n
		This command sets step width by which – with Dynamic Power Control being switched on - the channel power of the enhanced
		channels is increased or decreased. \n
			:param external: float Range: 0.5 to 6, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(external)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:DPControl:STEP:EXTernal {param}')
