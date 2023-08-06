from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Button:
	"""Button commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("button", core, parent)

	def get_brightness(self) -> int:
		"""DISPlay:BUTTon:BRIGhtness \n
		Sets the brightness of the [RF on/off] key. \n
			:return: button_brightnes: integer Range: 1 to 20
		"""
		response = self._core.io.query_str('DISPlay:BUTTon:BRIGhtness?')
		return Conversions.str_to_int(response)

	def set_brightness(self, button_brightnes: int) -> None:
		"""DISPlay:BUTTon:BRIGhtness \n
		Sets the brightness of the [RF on/off] key. \n
			:param button_brightnes: integer Range: 1 to 20
		"""
		param = Conversions.decimal_value_to_str(button_brightnes)
		self._core.io.write(f'DISPlay:BUTTon:BRIGhtness {param}')
