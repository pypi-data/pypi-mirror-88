from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class File:
	"""File commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("file", core, parent)

	def set(self, filename: str, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:A<CH>:APATtern:FILE \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.ant_pat/*.
		body_mask. Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in
		the default and in a specific directory. \n
			:param filename: 'filename' Filename or complete file path; file extension can be omitted. Query the existing files with the following commands: method RsSmbv.Source.Bb.Gnss.Apattern.Catalog.predefined method RsSmbv.Source.Bb.Gnss.Apattern.Catalog.user
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')"""
		param = Conversions.value_to_quoted_str(filename)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:A{channel_cmd_val}:APATtern:FILE {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> str:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:A<CH>:APATtern:FILE \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.ant_pat/*.
		body_mask. Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in
		the default and in a specific directory. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'A')
			:return: filename: 'filename' Filename or complete file path; file extension can be omitted. Query the existing files with the following commands: method RsSmbv.Source.Bb.Gnss.Apattern.Catalog.predefined method RsSmbv.Source.Bb.Gnss.Apattern.Catalog.user"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:A{channel_cmd_val}:APATtern:FILE?')
		return trim_str_response(response)
