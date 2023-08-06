from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScsMode:
	"""ScsMode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scsMode", core, parent)

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.AutoUser:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:BCH:SCSMode \n
		Queries the spreading code predetermined in the standard. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: scs_mode: AUTO"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:BCH:SCSMode?')
		return Conversions.str_to_scalar_enum(response, enums.AutoUser)
