from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Grid:
	"""Grid commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("grid", core, parent)

	def set(self, filename: str, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MOPS:IMPort<ST>:ADD:FILE:GRID<CH> \n
		Add *.ems, *.nstb or *.iono_grid files to an import file list. \n
			:param filename: string The Filename string comprises the file directory, filename and extension. For more information about *.ems and *.nstb files, see'SBAS correction file download links' . *.iono_grid files, see Example 'Ionospheric grid file content (extract) '.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'ImportPy')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')"""
		param = Conversions.value_to_quoted_str(filename)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MOPS:IMPort{stream_cmd_val}:ADD:FILE:GRID{channel_cmd_val} {param}')
