from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Phr:
	"""Phr commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("phr", core, parent)

	# noinspection PyTypeChecker
	def get_drm(self) -> enums.HrpUwbPhrdAtaRateMode:
		"""[SOURce<HW>]:BB:HUWB:PHR:DRM \n
		Sets the data rate mode of the physical header. \n
			:return: data_rate_mode: BMLP| BMHP| HMLR| HMHR
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:PHR:DRM?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbPhrdAtaRateMode)

	def set_drm(self, data_rate_mode: enums.HrpUwbPhrdAtaRateMode) -> None:
		"""[SOURce<HW>]:BB:HUWB:PHR:DRM \n
		Sets the data rate mode of the physical header. \n
			:param data_rate_mode: BMLP| BMHP| HMLR| HMHR
		"""
		param = Conversions.enum_scalar_to_str(data_rate_mode, enums.HrpUwbPhrdAtaRateMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:PHR:DRM {param}')
