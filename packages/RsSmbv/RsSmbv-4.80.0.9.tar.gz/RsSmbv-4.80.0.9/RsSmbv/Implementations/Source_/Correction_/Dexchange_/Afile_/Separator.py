from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Separator:
	"""Separator commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("separator", core, parent)

	# noinspection PyTypeChecker
	def get_column(self) -> enums.DexchSepCol:
		"""[SOURce<HW>]:CORRection:DEXChange:AFILe:SEParator:COLumn \n
		Selects the separator between the frequency and level column of the ASCII table. \n
			:return: column: TABulator| SEMicolon| COMMa| SPACe
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:DEXChange:AFILe:SEParator:COLumn?')
		return Conversions.str_to_scalar_enum(response, enums.DexchSepCol)

	def set_column(self, column: enums.DexchSepCol) -> None:
		"""[SOURce<HW>]:CORRection:DEXChange:AFILe:SEParator:COLumn \n
		Selects the separator between the frequency and level column of the ASCII table. \n
			:param column: TABulator| SEMicolon| COMMa| SPACe
		"""
		param = Conversions.enum_scalar_to_str(column, enums.DexchSepCol)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:DEXChange:AFILe:SEParator:COLumn {param}')

	# noinspection PyTypeChecker
	def get_decimal(self) -> enums.DexchSepDec:
		"""[SOURce<HW>]:CORRection:DEXChange:AFILe:SEParator:DECimal \n
		Sets the decimal separator used in the ASCII data between '.' (decimal point) and ',' (comma) with floating-point
		numerals. \n
			:return: decimal: DOT| COMMa
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:DEXChange:AFILe:SEParator:DECimal?')
		return Conversions.str_to_scalar_enum(response, enums.DexchSepDec)

	def set_decimal(self, decimal: enums.DexchSepDec) -> None:
		"""[SOURce<HW>]:CORRection:DEXChange:AFILe:SEParator:DECimal \n
		Sets the decimal separator used in the ASCII data between '.' (decimal point) and ',' (comma) with floating-point
		numerals. \n
			:param decimal: DOT| COMMa
		"""
		param = Conversions.enum_scalar_to_str(decimal, enums.DexchSepDec)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:DEXChange:AFILe:SEParator:DECimal {param}')
