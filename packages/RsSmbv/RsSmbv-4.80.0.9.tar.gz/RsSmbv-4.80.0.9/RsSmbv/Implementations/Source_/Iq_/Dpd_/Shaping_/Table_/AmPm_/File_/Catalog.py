from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Catalog:
	"""Catalog commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("catalog", core, parent)

	def get(self, stream=repcap.Stream.Default) -> List[str]:
		"""[SOURce<HW>]:IQ:DPD<ST>:SHAPing:TABLe:AMPM:FILE:CATalog \n
		Queries the available table files in the default directory. Only files with the extension *.dpd_magn(AM/AM) or *.
		dpd_phase(AM/PM) are listed. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')
			:return: catalog: string"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:SHAPing:TABLe:AMPM:FILE:CATalog?')
		return Conversions.str_to_str_list(response)
