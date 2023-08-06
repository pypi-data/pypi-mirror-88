from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Res:
	"""Res commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("res", core, parent)

	# noinspection PyTypeChecker
	def get_color(self) -> enums.Colour:
		"""TEST:RES:COLor \n
		No command help available \n
			:return: color: No help available
		"""
		response = self._core.io.query_str('TEST:RES:COLor?')
		return Conversions.str_to_scalar_enum(response, enums.Colour)

	def set_color(self, color: enums.Colour) -> None:
		"""TEST:RES:COLor \n
		No command help available \n
			:param color: No help available
		"""
		param = Conversions.enum_scalar_to_str(color, enums.Colour)
		self._core.io.write(f'TEST:RES:COLor {param}')

	def get_text(self) -> str:
		"""TEST:RES:TEXT \n
		No command help available \n
			:return: text: No help available
		"""
		response = self._core.io.query_str('TEST:RES:TEXT?')
		return trim_str_response(response)

	def set_text(self, text: str) -> None:
		"""TEST:RES:TEXT \n
		No command help available \n
			:param text: No help available
		"""
		param = Conversions.value_to_quoted_str(text)
		self._core.io.write(f'TEST:RES:TEXT {param}')

	def get_wind(self) -> bool:
		"""TEST:RES:WIND \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('TEST:RES:WIND?')
		return Conversions.str_to_bool(response)

	def set_wind(self, state: bool) -> None:
		"""TEST:RES:WIND \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'TEST:RES:WIND {param}')
