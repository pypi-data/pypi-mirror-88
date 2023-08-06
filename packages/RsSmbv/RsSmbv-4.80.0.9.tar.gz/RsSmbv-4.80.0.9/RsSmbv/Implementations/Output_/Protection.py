from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Protection:
	"""Protection commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("protection", core, parent)

	def clear(self) -> None:
		"""OUTPut<HW>:PROTection:CLEar \n
		Resets the protective circuit after it has been tripped. To define the output state, use the command
		:​OUTPut<hw>[:​STATe]. \n
		"""
		self._core.io.write(f'OUTPut<HwInstance>:PROTection:CLEar')

	def clear_with_opc(self) -> None:
		"""OUTPut<HW>:PROTection:CLEar \n
		Resets the protective circuit after it has been tripped. To define the output state, use the command
		:​OUTPut<hw>[:​STATe]. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'OUTPut<HwInstance>:PROTection:CLEar')

	def get_tripped(self) -> bool:
		"""OUTPut<HW>:PROTection:TRIPped \n
		Queries the state of the protective circuit. \n
			:return: tripped: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('OUTPut<HwInstance>:PROTection:TRIPped?')
		return Conversions.str_to_bool(response)
