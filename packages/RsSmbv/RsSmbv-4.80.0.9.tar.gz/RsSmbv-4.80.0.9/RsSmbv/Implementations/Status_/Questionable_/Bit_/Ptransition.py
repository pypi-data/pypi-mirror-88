from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ptransition:
	"""Ptransition commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ptransition", core, parent)

	def set(self, ptransition: str, bitNumber=repcap.BitNumber.Default) -> None:
		"""STATus:QUEStionable:BIT<BITNR>:PTRansition \n
		No command help available \n
			:param ptransition: No help available
			:param bitNumber: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bit')"""
		param = Conversions.value_to_quoted_str(ptransition)
		bitNumber_cmd_val = self._base.get_repcap_cmd_value(bitNumber, repcap.BitNumber)
		self._core.io.write(f'STATus:QUEStionable:BIT{bitNumber_cmd_val}:PTRansition {param}')

	def get(self, bitNumber=repcap.BitNumber.Default) -> str:
		"""STATus:QUEStionable:BIT<BITNR>:PTRansition \n
		No command help available \n
			:param bitNumber: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bit')
			:return: ptransition: No help available"""
		bitNumber_cmd_val = self._base.get_repcap_cmd_value(bitNumber, repcap.BitNumber)
		response = self._core.io.query_str(f'STATus:QUEStionable:BIT{bitNumber_cmd_val}:PTRansition?')
		return trim_str_response(response)
