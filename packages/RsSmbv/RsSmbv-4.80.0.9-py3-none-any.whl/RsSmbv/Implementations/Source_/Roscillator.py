from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Roscillator:
	"""Roscillator commands group definition. 12 total commands, 3 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("roscillator", core, parent)

	def clone(self) -> 'Roscillator':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Roscillator(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def external(self):
		"""external commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_external'):
			from .Roscillator_.External import External
			self._external = External(self._core, self._base)
		return self._external

	@property
	def output(self):
		"""output commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_output'):
			from .Roscillator_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	@property
	def internal(self):
		"""internal commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_internal'):
			from .Roscillator_.Internal import Internal
			self._internal = Internal(self._core, self._base)
		return self._internal

	def preset(self) -> None:
		"""[SOURce]:ROSCillator:PRESet \n
		Resets the reference oscillator settings. \n
		"""
		self._core.io.write(f'SOURce:ROSCillator:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce]:ROSCillator:PRESet \n
		Resets the reference oscillator settings. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce:ROSCillator:PRESet')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.SourceInt:
		"""[SOURce]:ROSCillator:SOURce \n
		Selects between internal or external reference frequency. \n
			:return: source: INTernal| EXTernal
		"""
		response = self._core.io.query_str('SOURce:ROSCillator:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SourceInt)

	def set_source(self, source: enums.SourceInt) -> None:
		"""[SOURce]:ROSCillator:SOURce \n
		Selects between internal or external reference frequency. \n
			:param source: INTernal| EXTernal
		"""
		param = Conversions.enum_scalar_to_str(source, enums.SourceInt)
		self._core.io.write(f'SOURce:ROSCillator:SOURce {param}')
