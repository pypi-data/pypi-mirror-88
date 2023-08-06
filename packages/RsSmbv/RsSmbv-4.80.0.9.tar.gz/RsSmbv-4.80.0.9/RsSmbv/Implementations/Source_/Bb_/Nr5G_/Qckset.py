from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Qckset:
	"""Qckset commands group definition. 27 total commands, 4 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("qckset", core, parent)

	def clone(self) -> 'Qckset':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Qckset(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Qckset_.Apply import Apply
			self._apply = Apply(self._core, self._base)
		return self._apply

	@property
	def discard(self):
		"""discard commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_discard'):
			from .Qckset_.Discard import Discard
			self._discard = Discard(self._core, self._base)
		return self._discard

	@property
	def frmFormat(self):
		"""frmFormat commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_frmFormat'):
			from .Qckset_.FrmFormat import FrmFormat
			self._frmFormat = FrmFormat(self._core, self._base)
		return self._frmFormat

	@property
	def general(self):
		"""general commands group. 1 Sub-classes, 8 commands."""
		if not hasattr(self, '_general'):
			from .Qckset_.General import General
			self._general = General(self._core, self._base)
		return self._general

	def set_state(self, qck_set_state: enums.QuickSetStateAll) -> None:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:STATe \n
		No command help available \n
			:param qck_set_state: No help available
		"""
		param = Conversions.enum_scalar_to_str(qck_set_state, enums.QuickSetStateAll)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:STATe {param}')
