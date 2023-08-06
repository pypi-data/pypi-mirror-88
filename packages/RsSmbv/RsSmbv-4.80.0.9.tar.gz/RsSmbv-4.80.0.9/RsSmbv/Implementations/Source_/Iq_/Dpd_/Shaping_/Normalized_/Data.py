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
		"""[SOURce<HW>]:IQ:DPD<ST>:SHAPing:NORMalized:DATA \n
		Defines the normalized predistortion function in a raw data format (binary data) . \n
			:param data: #LengthNoBytesNoBytesNormData # The binary data must start with the sign # LengthNoBytes ASCII format Sets the length of NoBytes, i.e. the number of digits used to write NoBytes NoBytes An ASCII integer value that specifies the number of bytes that follow in the NormData part Each of the NormData parameters is coded with 8 bytes. Then the number of bytes NoBytes is calculated as: NoBytes = 8 + 8 + n(8+8+8) , where n is the number of points NoPoints. NormData PinMaxNoPoints{VinVmaxDeltaVDeltaPhase} Values in binary format, describing the maximum absolute input power Pinmax, the number of subsequent points n and the normalized values Vin/Vmax, ΔV/V, ΔPhase [deg].
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_bin_block(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:SHAPing:NORMalized:DATA ', data)

	def get(self, stream=repcap.Stream.Default) -> bytes:
		"""[SOURce<HW>]:IQ:DPD<ST>:SHAPing:NORMalized:DATA \n
		Defines the normalized predistortion function in a raw data format (binary data) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')
			:return: data: #LengthNoBytesNoBytesNormData # The binary data must start with the sign # LengthNoBytes ASCII format Sets the length of NoBytes, i.e. the number of digits used to write NoBytes NoBytes An ASCII integer value that specifies the number of bytes that follow in the NormData part Each of the NormData parameters is coded with 8 bytes. Then the number of bytes NoBytes is calculated as: NoBytes = 8 + 8 + n(8+8+8) , where n is the number of points NoPoints. NormData PinMaxNoPoints{VinVmaxDeltaVDeltaPhase} Values in binary format, describing the maximum absolute input power Pinmax, the number of subsequent points n and the normalized values Vin/Vmax, ΔV/V, ΔPhase [deg]."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_bin_block_ERROR(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:SHAPing:NORMalized:DATA?')
		return response

	def load(self, filename: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DPD<ST>:SHAPing:NORMalized:DATA:LOAD \n
		Loads the selected file. \n
			:param filename: string
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')"""
		param = Conversions.value_to_quoted_str(filename)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:SHAPing:NORMalized:DATA:LOAD {param}')
