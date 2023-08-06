from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class File:
	"""File commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("file", core, parent)

	def set(self, filename: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SV:IMPort:SBAS:WAAS<ST>:ADD:FILE \n
		Adds *.ems files for EGNOS correction data *.nstb files for WAAS correction data to an import file list. \n
			:param filename: string The Filename string comprises the file directory, filename and extension. For more information about *.ems and *.nstb files, see 'SBAS correction file download links'.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbas')"""
		param = Conversions.value_to_quoted_str(filename)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:IMPort:SBAS:WAAS{stream_cmd_val}:ADD:FILE {param}')
