from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ulist:
	"""Ulist commands group definition. 4 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ulist", core, parent)

	def clone(self) -> 'Ulist':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ulist(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Ulist_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	@property
	def store(self):
		"""store commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_store'):
			from .Ulist_.Store import Store
			self._store = Store(self._core, self._base)
		return self._store

	def delete(self, filename: str, frameIx=repcap.FrameIx.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:FRAMe<DI>:ULISt:DELete \n
		This command deletes the selected file with user defined frame settings. The directory is set using command method RsSmbv.
		MassMemory.currentDirectory. A path can also be specified, in which case the files in the specified directory are read.
		The file extension can be omitted. Only files with the file extension *.gsm_fu and *.gsm_hfu are deleted. \n
			:param filename: string
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')"""
		param = Conversions.value_to_quoted_str(filename)
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:ULISt:DELete {param}')

	def load(self, filename: str, frameIx=repcap.FrameIx.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:FRAMe<DI>:ULISt:LOAD \n
		This command loads the selected file with user defined frame settings. The directory is set using command method RsSmbv.
		MassMemory.currentDirectory. A path can also be specified, in which case the files in the specified directory are read.
		The file extension can be omitted. Only files with the file extension *.gsm_fu and *.gsm_hfu are loaded. \n
			:param filename: string
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')"""
		param = Conversions.value_to_quoted_str(filename)
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:ULISt:LOAD {param}')
