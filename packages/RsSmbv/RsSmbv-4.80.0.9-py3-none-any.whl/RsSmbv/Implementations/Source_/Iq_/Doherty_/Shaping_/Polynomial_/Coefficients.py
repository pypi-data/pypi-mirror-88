from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coefficients:
	"""Coefficients commands group definition. 4 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coefficients", core, parent)

	def clone(self) -> 'Coefficients':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Coefficients(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Coefficients_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	@property
	def store(self):
		"""store commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_store'):
			from .Coefficients_.Store import Store
			self._store = Store(self._core, self._base)
		return self._store

	# noinspection PyTypeChecker
	class CoefficientsStruct(StructBase):
		"""Structure for setting input parameters. Fields: \n
			- Ipart_0: List[float]: No parameter help available
			- J_0: float: No parameter help available
			- I_1: float: No parameter help available
			- J_1: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Ipart_0', DataType.FloatList, None, False, True, 1),
			ArgStruct.scalar_float('J_0'),
			ArgStruct.scalar_float('I_1'),
			ArgStruct.scalar_float('J_1')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ipart_0: List[float] = None
			self.J_0: float = None
			self.I_1: float = None
			self.J_1: float = None

	def set(self, structure: CoefficientsStruct, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DOHerty<ST>:SHAPing:POLYnomial:COEFficients \n
		No command help available \n
			:param structure: for set value, see the help for CoefficientsStruct structure arguments.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write_struct(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SHAPing:POLYnomial:COEFficients', structure)

	def get(self, stream=repcap.Stream.Default) -> CoefficientsStruct:
		"""[SOURce<HW>]:IQ:DOHerty<ST>:SHAPing:POLYnomial:COEFficients \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')
			:return: structure: for return value, see the help for CoefficientsStruct structure arguments."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		return self._core.io.query_struct(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SHAPing:POLYnomial:COEFficients?', self.__class__.CoefficientsStruct())

	def load(self, filename: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DOHerty<ST>:SHAPing:POLYnomial:COEFficients:LOAD \n
		No command help available \n
			:param filename: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')"""
		param = Conversions.value_to_quoted_str(filename)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SHAPing:POLYnomial:COEFficients:LOAD {param}')
