from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Event:
	"""Event commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("event", core, parent)

	def get(self, bitNumber=repcap.BitNumber.Default) -> str:
		"""STATus:OPERation:BIT<BITNR>:[EVENt] \n
		No command help available \n
			:param bitNumber: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bit')
			:return: event: No help available"""
		bitNumber_cmd_val = self._base.get_repcap_cmd_value(bitNumber, repcap.BitNumber)
		response = self._core.io.query_str(f'STATus:OPERation:BIT{bitNumber_cmd_val}:EVENt?')
		return trim_str_response(response)
