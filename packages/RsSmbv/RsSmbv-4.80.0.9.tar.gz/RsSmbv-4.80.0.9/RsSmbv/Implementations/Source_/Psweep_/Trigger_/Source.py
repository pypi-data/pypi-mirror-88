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
		"""[SOURce<HW>]:PSWeep:TRIGger:SOURce:ADVanced \n
		No command help available \n
			:return: ps_trig_source_adv: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PSWeep:TRIGger:SOURce:ADVanced?')
		return Conversions.str_to_scalar_enum(response, enums.TrigSweepImmBusExt)

	def set_advanced(self, ps_trig_source_adv: enums.TrigSweepImmBusExt) -> None:
		"""[SOURce<HW>]:PSWeep:TRIGger:SOURce:ADVanced \n
		No command help available \n
			:param ps_trig_source_adv: No help available
		"""
		param = Conversions.enum_scalar_to_str(ps_trig_source_adv, enums.TrigSweepImmBusExt)
		self._core.io.write(f'SOURce<HwInstance>:PSWeep:TRIGger:SOURce:ADVanced {param}')
