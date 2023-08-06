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

	def set(self, filename: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:VEHicle:FILE \n
		Selects a predefined or user-defined vehicle description (*.xvd) file. \n
			:param filename: Filename or complete file path; file extension is optional Query the existing files with: method RsSmbv.Source.Bb.Gnss.Vehicle.Catalog.predefined method RsSmbv.Source.Bb.Gnss.Vehicle.Catalog.user
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.value_to_quoted_str(filename)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:LOCation:VEHicle:FILE {param}')

	def get(self, stream=repcap.Stream.Default) -> str:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:LOCation:VEHicle:FILE \n
		Selects a predefined or user-defined vehicle description (*.xvd) file. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: filename: Filename or complete file path; file extension is optional Query the existing files with: method RsSmbv.Source.Bb.Gnss.Vehicle.Catalog.predefined method RsSmbv.Source.Bb.Gnss.Vehicle.Catalog.user"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:LOCation:VEHicle:FILE?')
		return trim_str_response(response)
