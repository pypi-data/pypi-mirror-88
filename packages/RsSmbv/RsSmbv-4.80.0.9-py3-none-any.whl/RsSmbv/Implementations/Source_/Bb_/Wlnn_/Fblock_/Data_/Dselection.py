from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dselection:
	"""Dselection commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dselection", core, parent)

	def set(self, dselection: str, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:DATA:DSELection \n
		Selects the data list for the DLISt data source selection. The lists are stored as files with the fixed file extensions *.
		dm_iqd in a directory of the user's choice. The directory applicable to the following commands is defined with the
		command method RsSmbv.MassMemory.currentDirectory. To access the files in this directory, you only have to give the file
		name without the path and the file extension. \n
			:param dselection: string
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.value_to_quoted_str(dselection)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:DATA:DSELection {param}')

	def get(self, channel=repcap.Channel.Default) -> str:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:DATA:DSELection \n
		Selects the data list for the DLISt data source selection. The lists are stored as files with the fixed file extensions *.
		dm_iqd in a directory of the user's choice. The directory applicable to the following commands is defined with the
		command method RsSmbv.MassMemory.currentDirectory. To access the files in this directory, you only have to give the file
		name without the path and the file extension. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: dselection: string"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:DATA:DSELection?')
		return trim_str_response(response)
