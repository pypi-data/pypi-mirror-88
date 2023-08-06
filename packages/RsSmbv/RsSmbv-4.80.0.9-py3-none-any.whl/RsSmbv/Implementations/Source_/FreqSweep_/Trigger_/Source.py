from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("source", core, parent)

	# noinspection PyTypeChecker
	def get_advanced(self) -> enums.TrigSweepImmBusExt:
		"""[SOURce<HW>]:FSWeep:TRIGger:SOURce:ADVanced \n
		No command help available \n
			:return: imm_bus_ext: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FSWeep:TRIGger:SOURce:ADVanced?')
		return Conversions.str_to_scalar_enum(response, enums.TrigSweepImmBusExt)

	def set_advanced(self, imm_bus_ext: enums.TrigSweepImmBusExt) -> None:
		"""[SOURce<HW>]:FSWeep:TRIGger:SOURce:ADVanced \n
		No command help available \n
			:param imm_bus_ext: No help available
		"""
		param = Conversions.enum_scalar_to_str(imm_bus_ext, enums.TrigSweepImmBusExt)
		self._core.io.write(f'SOURce<HwInstance>:FSWeep:TRIGger:SOURce:ADVanced {param}')
