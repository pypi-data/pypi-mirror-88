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

	def get(self, channel=repcap.Channel.Default) -> List[str]:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:DG:SUSer:CATalog \n
		Queries the names of the existing user defined/predefined GBAS/SCAT-I differential files. Per default, the instrument
		stores user-defined files in the /var/user/ directory. Use the command method RsSmbv.MassMemory.currentDirectory to
		change the default directory to the currently used one. For GBAS differential files, files with extension *.rs_gbas are
		listed. For SCAT-I differential files, files with extension *.rs_scat are listed. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: gbas_mc_scat_differ_cat_name_user: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:DG:SUSer:CATalog?')
		return Conversions.str_to_str_list(response)
