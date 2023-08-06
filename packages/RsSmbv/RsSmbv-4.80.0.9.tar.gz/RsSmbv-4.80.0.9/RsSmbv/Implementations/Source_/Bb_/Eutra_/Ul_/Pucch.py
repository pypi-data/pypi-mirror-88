from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pucch:
	"""Pucch commands group definition. 10 total commands, 6 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pucch", core, parent)

	def clone(self) -> 'Pucch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pucch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def n1Emax(self):
		"""n1Emax commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n1Emax'):
			from .Pucch_.N1Emax import N1Emax
			self._n1Emax = N1Emax(self._core, self._base)
		return self._n1Emax

	@property
	def n1Nmax(self):
		"""n1Nmax commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n1Nmax'):
			from .Pucch_.N1Nmax import N1Nmax
			self._n1Nmax = N1Nmax(self._core, self._base)
		return self._n1Nmax

	@property
	def n2Max(self):
		"""n2Max commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n2Max'):
			from .Pucch_.N2Max import N2Max
			self._n2Max = N2Max(self._core, self._base)
		return self._n2Max

	@property
	def n3Max(self):
		"""n3Max commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n3Max'):
			from .Pucch_.N3Max import N3Max
			self._n3Max = N3Max(self._core, self._base)
		return self._n3Max

	@property
	def n4Max(self):
		"""n4Max commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n4Max'):
			from .Pucch_.N4Max import N4Max
			self._n4Max = N4Max(self._core, self._base)
		return self._n4Max

	@property
	def n5Max(self):
		"""n5Max commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n5Max'):
			from .Pucch_.N5Max import N5Max
			self._n5Max = N5Max(self._core, self._base)
		return self._n5Max

	def get_de_shift(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUCCh:DESHift \n
		Sets the delta shift parameter. \n
			:return: delta_shift: integer Range: 1 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PUCCh:DESHift?')
		return Conversions.str_to_int(response)

	def set_de_shift(self, delta_shift: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUCCh:DESHift \n
		Sets the delta shift parameter. \n
			:param delta_shift: integer Range: 1 to 3
		"""
		param = Conversions.decimal_value_to_str(delta_shift)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PUCCh:DESHift {param}')

	def get_n_1_cs(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUCCh:N1CS \n
		Sets the number of cyclic shifts used for PUCCH format 1/1a/1b in a resource block used for a combination of the formats
		1/1a/1b and 2/2a/2b. \n
			:return: n_1_cs: integer Range: 0 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PUCCh:N1CS?')
		return Conversions.str_to_int(response)

	def set_n_1_cs(self, n_1_cs: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUCCh:N1CS \n
		Sets the number of cyclic shifts used for PUCCH format 1/1a/1b in a resource block used for a combination of the formats
		1/1a/1b and 2/2a/2b. \n
			:param n_1_cs: integer Range: 0 to dynamic
		"""
		param = Conversions.decimal_value_to_str(n_1_cs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PUCCh:N1CS {param}')

	def get_n_2_rb(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUCCh:N2RB \n
		Sets bandwidth in terms of resource blocks that are reserved for PUCCH formats 2/2a/2b transmission in each subframe. \n
			:return: n_2_rb: integer Range: 0 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PUCCh:N2RB?')
		return Conversions.str_to_int(response)

	def set_n_2_rb(self, n_2_rb: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUCCh:N2RB \n
		Sets bandwidth in terms of resource blocks that are reserved for PUCCH formats 2/2a/2b transmission in each subframe. \n
			:param n_2_rb: integer Range: 0 to dynamic
		"""
		param = Conversions.decimal_value_to_str(n_2_rb)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PUCCh:N2RB {param}')

	def get_norb(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUCCh:NORB \n
		Sets the PUCCH region in terms of reserved resource blocks, at the edges of the channel bandwidth. \n
			:return: rb_count: integer Range: 0 to 110
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:UL:PUCCh:NORB?')
		return Conversions.str_to_int(response)

	def set_norb(self, rb_count: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PUCCh:NORB \n
		Sets the PUCCH region in terms of reserved resource blocks, at the edges of the channel bandwidth. \n
			:param rb_count: integer Range: 0 to 110
		"""
		param = Conversions.decimal_value_to_str(rb_count)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PUCCh:NORB {param}')
