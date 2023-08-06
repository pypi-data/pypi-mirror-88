from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mac:
	"""Mac commands group definition. 29 total commands, 10 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mac", core, parent)

	def clone(self) -> 'Mac':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mac(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def address(self):
		"""address commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_address'):
			from .Mac_.Address import Address
			self._address = Address(self._core, self._base)
		return self._address

	@property
	def did(self):
		"""did commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_did'):
			from .Mac_.Did import Did
			self._did = Did(self._core, self._base)
		return self._did

	@property
	def fcontrol(self):
		"""fcontrol commands group. 11 Sub-classes, 1 commands."""
		if not hasattr(self, '_fcontrol'):
			from .Mac_.Fcontrol import Fcontrol
			self._fcontrol = Fcontrol(self._core, self._base)
		return self._fcontrol

	@property
	def fcs(self):
		"""fcs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fcs'):
			from .Mac_.Fcs import Fcs
			self._fcs = Fcs(self._core, self._base)
		return self._fcs

	@property
	def heControl(self):
		"""heControl commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_heControl'):
			from .Mac_.HeControl import HeControl
			self._heControl = HeControl(self._core, self._base)
		return self._heControl

	@property
	def htControl(self):
		"""htControl commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_htControl'):
			from .Mac_.HtControl import HtControl
			self._htControl = HtControl(self._core, self._base)
		return self._htControl

	@property
	def qsControl(self):
		"""qsControl commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_qsControl'):
			from .Mac_.QsControl import QsControl
			self._qsControl = QsControl(self._core, self._base)
		return self._qsControl

	@property
	def scontrol(self):
		"""scontrol commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_scontrol'):
			from .Mac_.Scontrol import Scontrol
			self._scontrol = Scontrol(self._core, self._base)
		return self._scontrol

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Mac_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def vhtControl(self):
		"""vhtControl commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_vhtControl'):
			from .Mac_.VhtControl import VhtControl
			self._vhtControl = VhtControl(self._core, self._base)
		return self._vhtControl
