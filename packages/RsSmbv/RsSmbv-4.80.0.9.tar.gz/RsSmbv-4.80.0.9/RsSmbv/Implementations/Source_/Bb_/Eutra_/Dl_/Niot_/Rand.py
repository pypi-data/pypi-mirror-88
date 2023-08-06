from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rand:
	"""Rand commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rand", core, parent)

	# noinspection PyTypeChecker
	def get_rmax(self) -> enums.EutraNbiotRmAx:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:RAND:RMAX \n
		Sets the maximum number NPDCCH is repeated RMax (random access) . \n
			:return: random_rmax: R1| R2| R4| R8| R16| R32| R64| R128| R256| R512| R1024| R2048
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:RAND:RMAX?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotRmAx)

	def set_rmax(self, random_rmax: enums.EutraNbiotRmAx) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:RAND:RMAX \n
		Sets the maximum number NPDCCH is repeated RMax (random access) . \n
			:param random_rmax: R1| R2| R4| R8| R16| R32| R64| R128| R256| R512| R1024| R2048
		"""
		param = Conversions.enum_scalar_to_str(random_rmax, enums.EutraNbiotRmAx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:RAND:RMAX {param}')

	# noinspection PyTypeChecker
	def get_ss_offset(self) -> enums.EutraNbiotSearchSpaceOffset:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:RAND:SSOFfset \n
		Sets the serach space offset (ɑoffset) . \n
			:return: random_offset: O0| O1_8| O1_4| O3_8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:RAND:SSOFfset?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotSearchSpaceOffset)

	def set_ss_offset(self, random_offset: enums.EutraNbiotSearchSpaceOffset) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:RAND:SSOFfset \n
		Sets the serach space offset (ɑoffset) . \n
			:param random_offset: O0| O1_8| O1_4| O3_8
		"""
		param = Conversions.enum_scalar_to_str(random_offset, enums.EutraNbiotSearchSpaceOffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:RAND:SSOFfset {param}')

	# noinspection PyTypeChecker
	def get_sts_frame(self) -> enums.EutraNbiotSearchSpaceStSubframe:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:RAND:STSFrame \n
		Sets the start SF for the random access common search space. \n
			:return: start_sf: S1_5| S2| S4| S8| S16| S32| S48| S64
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NIOT:RAND:STSFrame?')
		return Conversions.str_to_scalar_enum(response, enums.EutraNbiotSearchSpaceStSubframe)

	def set_sts_frame(self, start_sf: enums.EutraNbiotSearchSpaceStSubframe) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:RAND:STSFrame \n
		Sets the start SF for the random access common search space. \n
			:param start_sf: S1_5| S2| S4| S8| S16| S32| S48| S64
		"""
		param = Conversions.enum_scalar_to_str(start_sf, enums.EutraNbiotSearchSpaceStSubframe)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:RAND:STSFrame {param}')
