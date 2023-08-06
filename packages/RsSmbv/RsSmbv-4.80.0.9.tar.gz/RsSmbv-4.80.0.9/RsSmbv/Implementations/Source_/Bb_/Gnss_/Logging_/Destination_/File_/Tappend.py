from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tappend:
	"""Tappend commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tappend", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:DESTination:FILE:TAPPend:[STATe] \n
		Adds a timestamp to the filename. \n
			:return: append: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:LOGGing:DESTination:FILE:TAPPend:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, append: bool) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:DESTination:FILE:TAPPend:[STATe] \n
		Adds a timestamp to the filename. \n
			:param append: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(append)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:DESTination:FILE:TAPPend:STATe {param}')
