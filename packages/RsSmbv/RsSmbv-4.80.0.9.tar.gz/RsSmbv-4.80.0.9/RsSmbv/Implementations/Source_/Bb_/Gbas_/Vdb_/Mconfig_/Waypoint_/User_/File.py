from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class File:
	"""File commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("file", core, parent)

	def set(self, filename: str, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:WAYPoint:USER:FILE \n
		Requires 'Mode > GBAS' (LAAS) header information. Loads the selected user-defined file (extension *.txt) . Per default,
		the instrument stores user-defined files in the /var/user/ directory. Use the command method RsSmbv.MassMemory.
		currentDirectory to change the default directory to the currently used one. \n
			:param filename: string For files stored in the default directory, only the file name is required.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.value_to_quoted_str(filename)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:WAYPoint:USER:FILE {param}')
