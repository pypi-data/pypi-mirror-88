from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApMap:
	"""ApMap commands group definition. 13 total commands, 13 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apMap", core, parent)

	def clone(self) -> 'ApMap':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ApMap(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ap1000Map(self):
		"""ap1000Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap1000Map'):
			from .ApMap_.Ap1000Map import Ap1000Map
			self._ap1000Map = Ap1000Map(self._core, self._base)
		return self._ap1000Map

	@property
	def ap100Map(self):
		"""ap100Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap100Map'):
			from .ApMap_.Ap100Map import Ap100Map
			self._ap100Map = Ap100Map(self._core, self._base)
		return self._ap100Map

	@property
	def ap1010Map(self):
		"""ap1010Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap1010Map'):
			from .ApMap_.Ap1010Map import Ap1010Map
			self._ap1010Map = Ap1010Map(self._core, self._base)
		return self._ap1010Map

	@property
	def ap1020Map(self):
		"""ap1020Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap1020Map'):
			from .ApMap_.Ap1020Map import Ap1020Map
			self._ap1020Map = Ap1020Map(self._core, self._base)
		return self._ap1020Map

	@property
	def ap10Map(self):
		"""ap10Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap10Map'):
			from .ApMap_.Ap10Map import Ap10Map
			self._ap10Map = Ap10Map(self._core, self._base)
		return self._ap10Map

	@property
	def ap200Map(self):
		"""ap200Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap200Map'):
			from .ApMap_.Ap200Map import Ap200Map
			self._ap200Map = Ap200Map(self._core, self._base)
		return self._ap200Map

	@property
	def ap201Map(self):
		"""ap201Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap201Map'):
			from .ApMap_.Ap201Map import Ap201Map
			self._ap201Map = Ap201Map(self._core, self._base)
		return self._ap201Map

	@property
	def ap20Map(self):
		"""ap20Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap20Map'):
			from .ApMap_.Ap20Map import Ap20Map
			self._ap20Map = Ap20Map(self._core, self._base)
		return self._ap20Map

	@property
	def ap21Map(self):
		"""ap21Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap21Map'):
			from .ApMap_.Ap21Map import Ap21Map
			self._ap21Map = Ap21Map(self._core, self._base)
		return self._ap21Map

	@property
	def ap40Map(self):
		"""ap40Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap40Map'):
			from .ApMap_.Ap40Map import Ap40Map
			self._ap40Map = Ap40Map(self._core, self._base)
		return self._ap40Map

	@property
	def ap41Map(self):
		"""ap41Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap41Map'):
			from .ApMap_.Ap41Map import Ap41Map
			self._ap41Map = Ap41Map(self._core, self._base)
		return self._ap41Map

	@property
	def ap42Map(self):
		"""ap42Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap42Map'):
			from .ApMap_.Ap42Map import Ap42Map
			self._ap42Map = Ap42Map(self._core, self._base)
		return self._ap42Map

	@property
	def ap43Map(self):
		"""ap43Map commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap43Map'):
			from .ApMap_.Ap43Map import Ap43Map
			self._ap43Map = Ap43Map(self._core, self._base)
		return self._ap43Map
