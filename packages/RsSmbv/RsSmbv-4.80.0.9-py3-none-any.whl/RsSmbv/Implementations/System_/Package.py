from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Package:
	"""Package commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("package", core, parent)

	def clone(self) -> 'Package':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Package(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def chartDisplay(self):
		"""chartDisplay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_chartDisplay'):
			from .Package_.ChartDisplay import ChartDisplay
			self._chartDisplay = ChartDisplay(self._core, self._base)
		return self._chartDisplay

	@property
	def guiFramework(self):
		"""guiFramework commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_guiFramework'):
			from .Package_.GuiFramework import GuiFramework
			self._guiFramework = GuiFramework(self._core, self._base)
		return self._guiFramework

	@property
	def qt(self):
		"""qt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qt'):
			from .Package_.Qt import Qt
			self._qt = Qt(self._core, self._base)
		return self._qt
