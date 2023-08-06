from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Users:
	"""Users commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("users", core, parent)

	def set(self, users: enums.TdscdmaTotalUsers, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:USERs \n
		Sets the total number of users of the cell. \n
			:param users: 2| 4| 6| 8| 10| 12| 14| 16
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(users, enums.TdscdmaTotalUsers)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:USERs {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.TdscdmaTotalUsers:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:USERs \n
		Sets the total number of users of the cell. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: users: 2| 4| 6| 8| 10| 12| 14| 16"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:USERs?')
		return Conversions.str_to_scalar_enum(response, enums.TdscdmaTotalUsers)
