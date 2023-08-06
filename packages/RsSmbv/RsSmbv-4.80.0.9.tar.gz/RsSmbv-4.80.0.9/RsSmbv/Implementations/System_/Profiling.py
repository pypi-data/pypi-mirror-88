from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Profiling:
	"""Profiling commands group definition. 11 total commands, 5 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("profiling", core, parent)

	def clone(self) -> 'Profiling':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Profiling(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def hwAccess(self):
		"""hwAccess commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_hwAccess'):
			from .Profiling_.HwAccess import HwAccess
			self._hwAccess = HwAccess(self._core, self._base)
		return self._hwAccess

	@property
	def logging(self):
		"""logging commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_logging'):
			from .Profiling_.Logging import Logging
			self._logging = Logging(self._core, self._base)
		return self._logging

	@property
	def module(self):
		"""module commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_module'):
			from .Profiling_.Module import Module
			self._module = Module(self._core, self._base)
		return self._module

	@property
	def tick(self):
		"""tick commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_tick'):
			from .Profiling_.Tick import Tick
			self._tick = Tick(self._core, self._base)
		return self._tick

	@property
	def tpoint(self):
		"""tpoint commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpoint'):
			from .Profiling_.Tpoint import Tpoint
			self._tpoint = Tpoint(self._core, self._base)
		return self._tpoint

	def get_state(self) -> bool:
		"""SYSTem:PROFiling:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SYSTem:PROFiling:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SYSTem:PROFiling:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SYSTem:PROFiling:STATe {param}')
