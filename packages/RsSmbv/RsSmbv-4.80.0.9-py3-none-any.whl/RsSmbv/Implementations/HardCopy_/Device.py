from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Device:
	"""Device commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("device", core, parent)

	# noinspection PyTypeChecker
	def get_language(self) -> enums.HcOpImgFormat:
		"""HCOPy:DEVice:LANGuage \n
		Selects the graphic format for the hard copy. You can use both commands alternatively. \n
			:return: language: BMP| JPG| XPM| PNG
		"""
		response = self._core.io.query_str('HCOPy:DEVice:LANGuage?')
		return Conversions.str_to_scalar_enum(response, enums.HcOpImgFormat)

	def set_language(self, language: enums.HcOpImgFormat) -> None:
		"""HCOPy:DEVice:LANGuage \n
		Selects the graphic format for the hard copy. You can use both commands alternatively. \n
			:param language: BMP| JPG| XPM| PNG
		"""
		param = Conversions.enum_scalar_to_str(language, enums.HcOpImgFormat)
		self._core.io.write(f'HCOPy:DEVice:LANGuage {param}')
