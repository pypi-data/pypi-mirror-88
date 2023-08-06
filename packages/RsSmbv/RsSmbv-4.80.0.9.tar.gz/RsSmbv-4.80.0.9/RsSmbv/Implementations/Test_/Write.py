from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Write:
	"""Write commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("write", core, parent)

	def set_result(self, result: enums.SelftLevWrite) -> None:
		"""TEST:WRITe:RESult \n
		No command help available \n
			:param result: No help available
		"""
		param = Conversions.enum_scalar_to_str(result, enums.SelftLevWrite)
		self._core.io.write(f'TEST:WRITe:RESult {param}')
