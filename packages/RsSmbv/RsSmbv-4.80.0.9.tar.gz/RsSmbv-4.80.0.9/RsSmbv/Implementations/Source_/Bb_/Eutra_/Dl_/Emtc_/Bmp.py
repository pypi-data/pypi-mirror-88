from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bmp:
	"""Bmp commands group definition. 5 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bmp", core, parent)

	def clone(self) -> 'Bmp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bmp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def valSubFrames(self):
		"""valSubFrames commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_valSubFrames'):
			from .Bmp_.ValSubFrames import ValSubFrames
			self._valSubFrames = ValSubFrames(self._core, self._base)
		return self._valSubFrames

	def get_pbchrep(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:PBCHrep \n
		Configures the cell for PBCH repetition. \n
			:return: pbch_repetitions: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:PBCHrep?')
		return Conversions.str_to_bool(response)

	def set_pbchrep(self, pbch_repetitions: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:PBCHrep \n
		Configures the cell for PBCH repetition. \n
			:param pbch_repetitions: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(pbch_repetitions)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:PBCHrep {param}')

	def get_sibbr(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:SIBBr \n
		Sets the number of times the PDSCH allocation carrying the SIB1-BR is repeated. \n
			:return: sched_info_sib_1_br: integer Range: 0 to 18
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:SIBBr?')
		return Conversions.str_to_int(response)

	def set_sibbr(self, sched_info_sib_1_br: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:SIBBr \n
		Sets the number of times the PDSCH allocation carrying the SIB1-BR is repeated. \n
			:param sched_info_sib_1_br: integer Range: 0 to 18
		"""
		param = Conversions.decimal_value_to_str(sched_info_sib_1_br)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:SIBBr {param}')

	# noinspection PyTypeChecker
	def get_start(self) -> enums.NumberA:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:STARt \n
		Defines the first symbol within a frame that can be used for eMTC. \n
			:return: starting_symbol: 1| 2| 3| 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:STARt?')
		return Conversions.str_to_scalar_enum(response, enums.NumberA)

	def set_start(self, starting_symbol: enums.NumberA) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:STARt \n
		Defines the first symbol within a frame that can be used for eMTC. \n
			:param starting_symbol: 1| 2| 3| 4
		"""
		param = Conversions.enum_scalar_to_str(starting_symbol, enums.NumberA)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:STARt {param}')

	# noinspection PyTypeChecker
	def get_sub_frames(self) -> enums.EutraBitmap:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:SUBFrames \n
		Sets the valid subframes configuration over 10ms or 40ms. \n
			:return: bitmap_subframes: 10| 40
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:SUBFrames?')
		return Conversions.str_to_scalar_enum(response, enums.EutraBitmap)

	def set_sub_frames(self, bitmap_subframes: enums.EutraBitmap) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:BMP:SUBFrames \n
		Sets the valid subframes configuration over 10ms or 40ms. \n
			:param bitmap_subframes: 10| 40
		"""
		param = Conversions.enum_scalar_to_str(bitmap_subframes, enums.EutraBitmap)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:BMP:SUBFrames {param}')
