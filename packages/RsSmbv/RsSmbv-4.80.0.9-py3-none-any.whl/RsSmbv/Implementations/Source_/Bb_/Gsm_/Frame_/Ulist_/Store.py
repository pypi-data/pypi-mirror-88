from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Store:
	"""Store commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("store", core, parent)

	def set(self, filename: str, frameIx=repcap.FrameIx.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:FRAMe<DI>:ULISt:STORe \n
		This command stores the current frame settings into the selected file. The directory is set using command method RsSmbv.
		MassMemory.currentDirectory. A path can also be specified, in which case the files in the specified directory are read.
		Only enter the file name. User Standards are stored as files with the specific file extensions *.gsm_fu and *.gsm_hfu. \n
			:param filename: string
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')"""
		param = Conversions.value_to_quoted_str(filename)
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:ULISt:STORe {param}')
