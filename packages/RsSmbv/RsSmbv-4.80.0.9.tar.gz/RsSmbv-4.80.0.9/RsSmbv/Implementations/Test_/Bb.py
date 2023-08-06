from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bb:
	"""Bb commands group definition. 18 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bb", core, parent)

	def clone(self) -> 'Bb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bb(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bnc(self):
		"""bnc commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_bnc'):
			from .Bb_.Bnc import Bnc
			self._bnc = Bnc(self._core, self._base)
		return self._bnc

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 6 commands."""
		if not hasattr(self, '_data'):
			from .Bb_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def generator(self):
		"""generator commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_generator'):
			from .Bb_.Generator import Generator
			self._generator = Generator(self._core, self._base)
		return self._generator

	def get_connection(self) -> bool:
		"""TEST:BB:CONNection \n
		No command help available \n
			:return: connection: No help available
		"""
		response = self._core.io.query_str('TEST:BB:CONNection?')
		return Conversions.str_to_bool(response)
