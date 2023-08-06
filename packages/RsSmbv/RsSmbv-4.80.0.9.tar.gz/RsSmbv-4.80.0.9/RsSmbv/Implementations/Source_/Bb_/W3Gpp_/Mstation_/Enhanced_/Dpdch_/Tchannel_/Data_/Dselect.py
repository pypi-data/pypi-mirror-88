from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from ..........Internal.Utilities import trim_str_response
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dselect:
	"""Dselect commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dselect", core, parent)

	def set(self, dselect: str, transportChannel=repcap.TransportChannel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:DATA:DSELect \n
		The command selects the data list for the enhanced channels for the DLISt selection. The files are stored with the fixed
		file extensions *.dm_iqd in a directory of the user's choice. The directory applicable to the commands is defined with
		the command method RsSmbv.MassMemory.currentDirectory. To access the files in this directory, you only have to give the
		file name, without the path and the file extension. \n
			:param dselect: string
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')"""
		param = Conversions.value_to_quoted_str(dselect)
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:DATA:DSELect {param}')

	def get(self, transportChannel=repcap.TransportChannel.Default) -> str:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:DATA:DSELect \n
		The command selects the data list for the enhanced channels for the DLISt selection. The files are stored with the fixed
		file extensions *.dm_iqd in a directory of the user's choice. The directory applicable to the commands is defined with
		the command method RsSmbv.MassMemory.currentDirectory. To access the files in this directory, you only have to give the
		file name, without the path and the file extension. \n
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')
			:return: dselect: string"""
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:DATA:DSELect?')
		return trim_str_response(response)
