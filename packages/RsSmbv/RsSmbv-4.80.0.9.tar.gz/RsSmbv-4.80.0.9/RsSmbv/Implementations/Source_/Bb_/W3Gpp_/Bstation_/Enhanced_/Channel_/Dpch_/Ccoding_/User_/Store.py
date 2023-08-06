from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Store:
	"""Store commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("store", core, parent)

	def set(self, filename: str, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:CCODing:USER:STORe \n
		The command saves the current settings for channel coding as user channel coding in the specified file. The files are
		stored with the fixed file extensions *.3g_ccod_dl in a directory of the user's choice. The directory in which the file
		is stored is defined with the command method RsSmbv.MassMemory.currentDirectory. To store the files in this directory,
		you only have to give the file name, without the path and the file extension. \n
			:param filename: string
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.value_to_quoted_str(filename)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:CCODing:USER:STORe {param}')
