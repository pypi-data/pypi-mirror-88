from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Image:
	"""Image commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("image", core, parent)

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.HcOpImgFormat:
		"""HCOPy:IMAGe:FORMat \n
		Selects the graphic format for the hard copy. You can use both commands alternatively. \n
			:return: format_py: No help available
		"""
		response = self._core.io.query_str('HCOPy:IMAGe:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.HcOpImgFormat)

	def set_format_py(self, format_py: enums.HcOpImgFormat) -> None:
		"""HCOPy:IMAGe:FORMat \n
		Selects the graphic format for the hard copy. You can use both commands alternatively. \n
			:param format_py: BMP| JPG| XPM| PNG
		"""
		param = Conversions.enum_scalar_to_str(format_py, enums.HcOpImgFormat)
		self._core.io.write(f'HCOPy:IMAGe:FORMat {param}')
