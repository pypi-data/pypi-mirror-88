from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Correction:
	"""Correction commands group definition. 68 total commands, 4 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("correction", core, parent)

	def clone(self) -> 'Correction':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Correction(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cset(self):
		"""cset commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_cset'):
			from .Correction_.Cset import Cset
			self._cset = Cset(self._core, self._base)
		return self._cset

	@property
	def dexchange(self):
		"""dexchange commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_dexchange'):
			from .Correction_.Dexchange import Dexchange
			self._dexchange = Dexchange(self._core, self._base)
		return self._dexchange

	@property
	def fresponse(self):
		"""fresponse commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fresponse'):
			from .Correction_.Fresponse import Fresponse
			self._fresponse = Fresponse(self._core, self._base)
		return self._fresponse

	@property
	def zeroing(self):
		"""zeroing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zeroing'):
			from .Correction_.Zeroing import Zeroing
			self._zeroing = Zeroing(self._core, self._base)
		return self._zeroing

	def get_value(self) -> float:
		"""[SOURce<HW>]:CORRection:VALue \n
		Queries the current value for user correction. \n
			:return: value: float Range: -100 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:VALue?')
		return Conversions.str_to_float(response)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:CORRection:[STATe] \n
		Activates user correction with the currently selected table. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:CORRection:[STATe] \n
		Activates user correction with the currently selected table. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:STATe {param}')
