from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	def get_state(self) -> bool:
		"""OUTPut:ALL:[STATe] \n
		Activates the RF output signal of the instrument. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('OUTPut:ALL:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""OUTPut:ALL:[STATe] \n
		Activates the RF output signal of the instrument. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'OUTPut:ALL:STATe {param}')
