from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 4 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def clone(self) -> 'Data':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Data(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Data_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	@property
	def store(self):
		"""store commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_store'):
			from .Data_.Store import Store
			self._store = Store(self._core, self._base)
		return self._store

	def set(self, data: bytes, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DOHerty<ST>:SHAPing:NORMalized:DATA \n
		No command help available \n
			:param data: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_bin_block(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SHAPing:NORMalized:DATA ', data)

	def get(self, stream=repcap.Stream.Default) -> bytes:
		"""[SOURce<HW>]:IQ:DOHerty<ST>:SHAPing:NORMalized:DATA \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')
			:return: data: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_bin_block_ERROR(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SHAPing:NORMalized:DATA?')
		return response

	def load(self, filename: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DOHerty<ST>:SHAPing:NORMalized:DATA:LOAD \n
		No command help available \n
			:param filename: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')"""
		param = Conversions.value_to_quoted_str(filename)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SHAPing:NORMalized:DATA:LOAD {param}')
