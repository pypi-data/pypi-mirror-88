from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 17 total commands, 5 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("display", core, parent)

	def clone(self) -> 'Display':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Display(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def annotation(self):
		"""annotation commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_annotation'):
			from .Display_.Annotation import Annotation
			self._annotation = Annotation(self._core, self._base)
		return self._annotation

	@property
	def button(self):
		"""button commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_button'):
			from .Display_.Button import Button
			self._button = Button(self._core, self._base)
		return self._button

	@property
	def dialog(self):
		"""dialog commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_dialog'):
			from .Display_.Dialog import Dialog
			self._dialog = Dialog(self._core, self._base)
		return self._dialog

	@property
	def psave(self):
		"""psave commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_psave'):
			from .Display_.Psave import Psave
			self._psave = Psave(self._core, self._base)
		return self._psave

	@property
	def ukey(self):
		"""ukey commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_ukey'):
			from .Display_.Ukey import Ukey
			self._ukey = Ukey(self._core, self._base)
		return self._ukey

	def get_brightness(self) -> float:
		"""DISPlay:BRIGhtness \n
		Sets the brightness of the dispaly. \n
			:return: brightness: float Range: 1.0 to 20.0
		"""
		response = self._core.io.query_str('DISPlay:BRIGhtness?')
		return Conversions.str_to_float(response)

	def set_brightness(self, brightness: float) -> None:
		"""DISPlay:BRIGhtness \n
		Sets the brightness of the dispaly. \n
			:param brightness: float Range: 1.0 to 20.0
		"""
		param = Conversions.decimal_value_to_str(brightness)
		self._core.io.write(f'DISPlay:BRIGhtness {param}')

	def set_focus_object(self, obj_name: str) -> None:
		"""DISPlay:FOCusobject \n
		No command help available \n
			:param obj_name: No help available
		"""
		param = Conversions.value_to_quoted_str(obj_name)
		self._core.io.write(f'DISPlay:FOCusobject {param}')

	def set_message(self, message: str) -> None:
		"""DISPlay:MESSage \n
		No command help available \n
			:param message: No help available
		"""
		param = Conversions.value_to_quoted_str(message)
		self._core.io.write(f'DISPlay:MESSage {param}')

	def get_update(self) -> bool:
		"""DISPlay:UPDate \n
		Activates the refresh mode of the display. \n
			:return: update: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('DISPlay:UPDate?')
		return Conversions.str_to_bool(response)

	def set_update(self, update: bool) -> None:
		"""DISPlay:UPDate \n
		Activates the refresh mode of the display. \n
			:param update: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(update)
		self._core.io.write(f'DISPlay:UPDate {param}')
