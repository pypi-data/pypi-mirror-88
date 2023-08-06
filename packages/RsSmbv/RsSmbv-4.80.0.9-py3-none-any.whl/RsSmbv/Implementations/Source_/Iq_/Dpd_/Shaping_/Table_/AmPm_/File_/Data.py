from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def set(self, dpd_pm_table_data: List[float], stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DPD<ST>:SHAPing:TABLe:AMPM:FILE:DATA \n
		Defines the predistortion function in a raw data format. See also method RsSmbv.Source.Iq.Dpd.Shaping.Table.AmPm.File.New.
		set. \n
			:param dpd_pm_table_data: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')"""
		param = Conversions.list_to_csv_str(dpd_pm_table_data)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:SHAPing:TABLe:AMPM:FILE:DATA {param}')

	def get(self, stream=repcap.Stream.Default) -> List[float]:
		"""[SOURce<HW>]:IQ:DPD<ST>:SHAPing:TABLe:AMPM:FILE:DATA \n
		Defines the predistortion function in a raw data format. See also method RsSmbv.Source.Iq.Dpd.Shaping.Table.AmPm.File.New.
		set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')
			:return: dpd_pm_table_data: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_bin_or_ascii_float_list(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:SHAPing:TABLe:AMPM:FILE:DATA?')
		return response
