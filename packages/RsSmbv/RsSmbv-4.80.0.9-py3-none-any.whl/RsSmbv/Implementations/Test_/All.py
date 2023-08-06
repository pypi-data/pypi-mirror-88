from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	# noinspection PyTypeChecker
	def get_result(self) -> enums.Test:
		"""TEST<HW>:ALL:RESult \n
		Queries the result of the performed selftest. Start the selftest with method RsSmbv.Test.All.start. \n
			:return: result: 0| 1| RUNning| STOPped
		"""
		response = self._core.io.query_str('TEST<HwInstance>:ALL:RESult?')
		return Conversions.str_to_scalar_enum(response, enums.Test)

	def start(self) -> None:
		"""TEST<HW>:ALL:STARt \n
		No command help available \n
		"""
		self._core.io.write(f'TEST<HwInstance>:ALL:STARt')

	def start_with_opc(self) -> None:
		"""TEST<HW>:ALL:STARt \n
		No command help available \n
		Same as start, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'TEST<HwInstance>:ALL:STARt')
