from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PoCount:
	"""PoCount commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("poCount", core, parent)

	def get_set(self) -> int:
		"""DIAGnostic:INFO:POCount:SET \n
		No command help available \n
			:return: set_py: No help available
		"""
		response = self._core.io.query_str('DIAGnostic:INFO:POCount:SET?')
		return Conversions.str_to_int(response)

	def set_set(self, set_py: int) -> None:
		"""DIAGnostic:INFO:POCount:SET \n
		No command help available \n
			:param set_py: No help available
		"""
		param = Conversions.decimal_value_to_str(set_py)
		self._core.io.write(f'DIAGnostic:INFO:POCount:SET {param}')

	def get_value(self) -> int:
		"""DIAGnostic:INFO:POCount \n
		Queris how often the instrument has been turned on so far. \n
			:return: power_on_count: integer Range: 0 to INT_MAX
		"""
		response = self._core.io.query_str('DIAGnostic:INFO:POCount?')
		return Conversions.str_to_int(response)
