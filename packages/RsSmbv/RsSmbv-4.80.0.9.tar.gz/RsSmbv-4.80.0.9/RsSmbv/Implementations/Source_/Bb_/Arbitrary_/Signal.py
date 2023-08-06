from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Signal:
	"""Signal commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("signal", core, parent)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.ArbSignType:
		"""[SOURce<HW>]:BB:ARBitrary:SIGNal:TYPE \n
		Selects the type of test signal. \n
			:return: arb_signal_type: SINE| RECT| CIQ
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:SIGNal:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.ArbSignType)

	def set_type_py(self, arb_signal_type: enums.ArbSignType) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:SIGNal:TYPE \n
		Selects the type of test signal. \n
			:param arb_signal_type: SINE| RECT| CIQ
		"""
		param = Conversions.enum_scalar_to_str(arb_signal_type, enums.ArbSignType)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:SIGNal:TYPE {param}')
