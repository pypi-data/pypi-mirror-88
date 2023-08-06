from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Kboard:
	"""Kboard commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("kboard", core, parent)

	# noinspection PyTypeChecker
	def get_layout(self) -> enums.KbLayout:
		"""KBOard:LAYout \n
		Selects the language for an external keyboard and assigns the keys acccordingly. \n
			:return: layout: CHINese| DANish| DUTCh| DUTBe| ENGLish| ENGUK| FINNish| FRENch| FREBe| FRECa| GERMan| ITALian| JAPanese| KORean| NORWegian| PORTuguese| RUSSian| SPANish| SWEDish| ENGUS
		"""
		response = self._core.io.query_str('KBOard:LAYout?')
		return Conversions.str_to_scalar_enum(response, enums.KbLayout)

	def set_layout(self, layout: enums.KbLayout) -> None:
		"""KBOard:LAYout \n
		Selects the language for an external keyboard and assigns the keys acccordingly. \n
			:param layout: CHINese| DANish| DUTCh| DUTBe| ENGLish| ENGUK| FINNish| FRENch| FREBe| FRECa| GERMan| ITALian| JAPanese| KORean| NORWegian| PORTuguese| RUSSian| SPANish| SWEDish| ENGUS
		"""
		param = Conversions.enum_scalar_to_str(layout, enums.KbLayout)
		self._core.io.write(f'KBOard:LAYout {param}')
