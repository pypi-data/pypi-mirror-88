from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Impairment:
	"""Impairment commands group definition. 5 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("impairment", core, parent)

	def clone(self) -> 'Impairment':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Impairment(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def iqRatio(self):
		"""iqRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqRatio'):
			from .Impairment_.IqRatio import IqRatio
			self._iqRatio = IqRatio(self._core, self._base)
		return self._iqRatio

	@property
	def leakage(self):
		"""leakage commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_leakage'):
			from .Impairment_.Leakage import Leakage
			self._leakage = Leakage(self._core, self._base)
		return self._leakage

	@property
	def quadrature(self):
		"""quadrature commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_quadrature'):
			from .Impairment_.Quadrature import Quadrature
			self._quadrature = Quadrature(self._core, self._base)
		return self._quadrature

	def get_state(self) -> bool:
		"""[SOURce<HW>]:IQ:IMPairment:[STATe] \n
		Activates the impairment or correction values LEAKage, QUADrature and IQRatio for the corresponding stream. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:IMPairment:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:IQ:IMPairment:[STATe] \n
		Activates the impairment or correction values LEAKage, QUADrature and IQRatio for the corresponding stream. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:IMPairment:STATe {param}')
