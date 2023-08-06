from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Duration:
	"""Duration commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("duration", core, parent)

	# noinspection PyTypeChecker
	def get_coefficent(self) -> enums.EutraNbiotGapDurationCoefficent:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:GAP:DURation:COEFficent \n
		Sets the gap duration coefficient. \n
			:return: gap_dur_coeff: 1_8| 1_4| 3_8| 1_2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:GAP:DURation:COEFficent?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotGapDurationCoefficent)

	def set_coefficent(self, gap_dur_coeff: enums.EutraNbiotGapDurationCoefficent) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:GAP:DURation:COEFficent \n
		Sets the gap duration coefficient. \n
			:param gap_dur_coeff: 1_8| 1_4| 3_8| 1_2
		"""
		param = Conversions.enum_scalar_to_str(gap_dur_coeff, enums.EutraNbiotGapDurationCoefficent)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:GAP:DURation:COEFficent {param}')
