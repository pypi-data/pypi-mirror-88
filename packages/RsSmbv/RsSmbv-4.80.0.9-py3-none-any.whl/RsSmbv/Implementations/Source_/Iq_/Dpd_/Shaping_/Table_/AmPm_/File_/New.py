from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class New:
	"""New commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("new", core, parent)

	def set(self, ipartd_pi_db_dpd_pm_table_data_new_file: List[float], stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DPD<ST>:SHAPing:TABLe:AMPM:FILE:NEW \n
		Stores the correction values into a file with the selected file name and loads it. The file is stored in the default
		directory or in the directory specified with the absolute file path. If the file does not yet exist, a new file is
		created. The file extension is assigned automatically. \n
			:param ipartd_pi_db_dpd_pm_table_data_new_file: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')"""
		param = Conversions.list_to_csv_str(ipartd_pi_db_dpd_pm_table_data_new_file)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:SHAPing:TABLe:AMPM:FILE:NEW {param}')
