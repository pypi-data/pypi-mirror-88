from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ntransition:
	"""Ntransition commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ntransition", core, parent)

	def set(self, ntransition: str, bitNumber=repcap.BitNumber.Default) -> None:
		"""STATus:QUEStionable:BIT<BITNR>:NTRansition \n
		No command help available \n
			:param ntransition: No help available
			:param bitNumber: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bit')"""
		param = Conversions.value_to_quoted_str(ntransition)
		bitNumber_cmd_val = self._base.get_repcap_cmd_value(bitNumber, repcap.BitNumber)
		self._core.io.write(f'STATus:QUEStionable:BIT{bitNumber_cmd_val}:NTRansition {param}')

	def get(self, bitNumber=repcap.BitNumber.Default) -> str:
		"""STATus:QUEStionable:BIT<BITNR>:NTRansition \n
		No command help available \n
			:param bitNumber: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bit')
			:return: ntransition: No help available"""
		bitNumber_cmd_val = self._base.get_repcap_cmd_value(bitNumber, repcap.BitNumber)
		response = self._core.io.query_str(f'STATus:QUEStionable:BIT{bitNumber_cmd_val}:NTRansition?')
		return trim_str_response(response)
