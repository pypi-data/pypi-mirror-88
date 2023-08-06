from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AqPsk:
	"""AqPsk commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("aqPsk", core, parent)

	def clone(self) -> 'AqPsk':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AqPsk(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def angle(self):
		"""angle commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_angle'):
			from .AqPsk_.Angle import Angle
			self._angle = Angle(self._core, self._base)
		return self._angle

	@property
	def scpir(self):
		"""scpir commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scpir'):
			from .AqPsk_.Scpir import Scpir
			self._scpir = Scpir(self._core, self._base)
		return self._scpir

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.GsmModTypeAqpsk:
		"""[SOURce<HW>]:BB:GSM:AQPSk:FORMat \n
		The command queries the modulation type. The modulation type is permanently set to AQPSK. \n
			:return: format_py: AQPSk
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:AQPSk:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.GsmModTypeAqpsk)
