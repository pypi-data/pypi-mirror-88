from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sformat:
	"""Sformat commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sformat", core, parent)

	def get(self, stream=repcap.Stream.Default) -> str:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:BCH:SFORmat \n
		The command queries the slot format of the selected channel. A slot format defines the complete structure of a slot made
		of data and control fields and includes the symbol rate. The slot format (and thus the symbol rate, the pilot length, and
		the TFCI State) depends on the coding type selected. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: sf_ormat: string"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:BCH:SFORmat?')
		return trim_str_response(response)
