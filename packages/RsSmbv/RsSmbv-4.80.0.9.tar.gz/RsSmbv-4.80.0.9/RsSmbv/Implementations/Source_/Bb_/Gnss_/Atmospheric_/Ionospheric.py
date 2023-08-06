from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ionospheric:
	"""Ionospheric commands group definition. 17 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ionospheric", core, parent)

	def clone(self) -> 'Ionospheric':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ionospheric(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def klobuchar(self):
		"""klobuchar commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_klobuchar'):
			from .Ionospheric_.Klobuchar import Klobuchar
			self._klobuchar = Klobuchar(self._core, self._base)
		return self._klobuchar

	@property
	def mops(self):
		"""mops commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_mops'):
			from .Ionospheric_.Mops import Mops
			self._mops = Mops(self._core, self._base)
		return self._mops

	@property
	def neQuick(self):
		"""neQuick commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_neQuick'):
			from .Ionospheric_.NeQuick import NeQuick
			self._neQuick = NeQuick(self._core, self._base)
		return self._neQuick

	# noinspection PyTypeChecker
	def get_model(self) -> enums.IonModel:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MODel \n
		Determines the applied ionospheric model. \n
			:return: model: NONE| KLOBuchar| MOPS| NEQuick
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MODel?')
		return Conversions.str_to_scalar_enum(response, enums.IonModel)

	def set_model(self, model: enums.IonModel) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MODel \n
		Determines the applied ionospheric model. \n
			:param model: NONE| KLOBuchar| MOPS| NEQuick
		"""
		param = Conversions.enum_scalar_to_str(model, enums.IonModel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MODel {param}')
