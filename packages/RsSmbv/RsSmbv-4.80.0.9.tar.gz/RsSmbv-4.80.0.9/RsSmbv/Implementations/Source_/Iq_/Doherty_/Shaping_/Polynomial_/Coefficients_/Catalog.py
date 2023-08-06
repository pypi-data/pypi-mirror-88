from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	def get(self, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:IQ:DOHerty<ST>:SHAPing:POLYnomial:COEFficients:CATalog \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')
			:return: catalog: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SHAPing:POLYnomial:COEFficients:CATalog?')
		return Conversions.str_to_str_list(response)
