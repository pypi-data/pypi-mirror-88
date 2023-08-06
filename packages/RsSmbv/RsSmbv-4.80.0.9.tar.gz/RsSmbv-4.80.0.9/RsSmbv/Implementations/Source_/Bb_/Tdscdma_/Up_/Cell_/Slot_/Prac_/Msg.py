from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Msg:
	"""Msg commands group definition. 12 total commands, 10 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("msg", core, parent)

	def clone(self) -> 'Msg':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Msg(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Msg_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def length(self):
		"""length commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_length'):
			from .Msg_.Length import Length
			self._length = Length(self._core, self._base)
		return self._length

	@property
	def mshift(self):
		"""mshift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mshift'):
			from .Msg_.Mshift import Mshift
			self._mshift = Mshift(self._core, self._base)
		return self._mshift

	@property
	def pcorrection(self):
		"""pcorrection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pcorrection'):
			from .Msg_.Pcorrection import Pcorrection
			self._pcorrection = Pcorrection(self._core, self._base)
		return self._pcorrection

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Msg_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def scode(self):
		"""scode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scode'):
			from .Msg_.Scode import Scode
			self._scode = Scode(self._core, self._base)
		return self._scode

	@property
	def sfactor(self):
		"""sfactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfactor'):
			from .Msg_.Sfactor import Sfactor
			self._sfactor = Sfactor(self._core, self._base)
		return self._sfactor

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Msg_.Sformat import Sformat
			self._sformat = Sformat(self._core, self._base)
		return self._sformat

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Msg_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_user'):
			from .Msg_.User import User
			self._user = User(self._core, self._base)
		return self._user
