from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Loscillator:
	"""Loscillator commands group definition. 4 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("loscillator", core, parent)

	def clone(self) -> 'Loscillator':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Loscillator(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def inputPy(self):
		"""inputPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_inputPy'):
			from .Loscillator_.InputPy import InputPy
			self._inputPy = InputPy(self._core, self._base)
		return self._inputPy

	@property
	def output(self):
		"""output commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_output'):
			from .Loscillator_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.SourceInt:
		"""[SOURce<HW>]:FREQuency:LOSCillator:MODE \n
		Selects the mode of the local oscillator coupling. \n
			:return: mode: INTernal| EXTernal
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:FREQuency:LOSCillator:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SourceInt)

	def set_mode(self, mode: enums.SourceInt) -> None:
		"""[SOURce<HW>]:FREQuency:LOSCillator:MODE \n
		Selects the mode of the local oscillator coupling. \n
			:param mode: INTernal| EXTernal
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.SourceInt)
		self._core.io.write(f'SOURce<HwInstance>:FREQuency:LOSCillator:MODE {param}')
