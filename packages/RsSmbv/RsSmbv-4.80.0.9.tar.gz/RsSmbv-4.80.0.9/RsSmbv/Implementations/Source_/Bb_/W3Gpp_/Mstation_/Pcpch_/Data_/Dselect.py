from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dselect:
	"""Dselect commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dselect", core, parent)

	def set(self, dselect: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:DATA:DSELect \n
		The command selects the data list for the DLISt data source. The files are stored with the fixed file extensions *.dm_iqd
		in a directory of the user's choice. The directory applicable to the commands is defined with the command method RsSmbv.
		MassMemory.currentDirectory. To access the files in this directory, you only have to give the file name, without the path
		and the file extension. \n
			:param dselect: string
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.value_to_quoted_str(dselect)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:DATA:DSELect {param}')

	def get(self, stream=repcap.Stream.Default) -> str:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PCPCh:DATA:DSELect \n
		The command selects the data list for the DLISt data source. The files are stored with the fixed file extensions *.dm_iqd
		in a directory of the user's choice. The directory applicable to the commands is defined with the command method RsSmbv.
		MassMemory.currentDirectory. To access the files in this directory, you only have to give the file name, without the path
		and the file extension. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: dselect: string"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PCPCh:DATA:DSELect?')
		return trim_str_response(response)
