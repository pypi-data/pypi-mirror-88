from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Shaping:
	"""Shaping commands group definition. 23 total commands, 6 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("shaping", core, parent)

	def clone(self) -> 'Shaping':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Shaping(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_clipping'):
			from .Shaping_.Clipping import Clipping
			self._clipping = Clipping(self._core, self._base)
		return self._clipping

	@property
	def coefficients(self):
		"""coefficients commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_coefficients'):
			from .Shaping_.Coefficients import Coefficients
			self._coefficients = Coefficients(self._core, self._base)
		return self._coefficients

	@property
	def detroughing(self):
		"""detroughing commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_detroughing'):
			from .Shaping_.Detroughing import Detroughing
			self._detroughing = Detroughing(self._core, self._base)
		return self._detroughing

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_file'):
			from .Shaping_.File import File
			self._file = File(self._core, self._base)
		return self._file

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_gain'):
			from .Shaping_.Gain import Gain
			self._gain = Gain(self._core, self._base)
		return self._gain

	@property
	def pv(self):
		"""pv commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pv'):
			from .Shaping_.Pv import Pv
			self._pv = Pv(self._core, self._base)
		return self._pv

	# noinspection PyTypeChecker
	def get_interp(self) -> enums.Interpolation:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:INTerp \n
		For envelope shaping with shaping tables, enables linear interpolation. \n
			:return: ipartnterpolation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:INTerp?')
		return Conversions.str_to_scalar_enum(response, enums.Interpolation)

	def set_interp(self, ipartnterpolation: enums.Interpolation) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:INTerp \n
		For envelope shaping with shaping tables, enables linear interpolation. \n
			:param ipartnterpolation: OFF| LINear| POWer LINear = Linear (Voltage) POWer = Linear (Power)
		"""
		param = Conversions.enum_scalar_to_str(ipartnterpolation, enums.Interpolation)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:INTerp {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.IqOutEnvShapeMode:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:MODE \n
		Enables envelope shaping and selects the method to define the shaping function. \n
			:return: shaping_mode: OFF| LINear| TABLe| POLYnomial| DETRoughing| POWer LINear = Linear (Voltage) POWer = Linear (Power)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvShapeMode)

	def set_mode(self, shaping_mode: enums.IqOutEnvShapeMode) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:MODE \n
		Enables envelope shaping and selects the method to define the shaping function. \n
			:param shaping_mode: OFF| LINear| TABLe| POLYnomial| DETRoughing| POWer LINear = Linear (Voltage) POWer = Linear (Power)
		"""
		param = Conversions.enum_scalar_to_str(shaping_mode, enums.IqOutEnvShapeMode)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:MODE {param}')

	# noinspection PyTypeChecker
	def get_scale(self) -> enums.IqOutEnvScale:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:SCALe \n
		Determines the units used on the x and y axis. \n
			:return: scale: POWer| VOLTage
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:SCALe?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutEnvScale)

	def set_scale(self, scale: enums.IqOutEnvScale) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:SCALe \n
		Determines the units used on the x and y axis. \n
			:param scale: POWer| VOLTage
		"""
		param = Conversions.enum_scalar_to_str(scale, enums.IqOutEnvScale)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:SCALe {param}')
