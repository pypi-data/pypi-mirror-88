from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tchannel:
	"""Tchannel commands group definition. 6 total commands, 4 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tchannel", core, parent)

	def clone(self) -> 'Tchannel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tchannel(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Tchannel_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dcChannel(self):
		"""dcChannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dcChannel'):
			from .Tchannel_.DcChannel import DcChannel
			self._dcChannel = DcChannel(self._core, self._base)
		return self._dcChannel

	@property
	def fchannel(self):
		"""fchannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fchannel'):
			from .Tchannel_.Fchannel import Fchannel
			self._fchannel = Fchannel(self._core, self._base)
		return self._fchannel

	@property
	def schannel(self):
		"""schannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_schannel'):
			from .Tchannel_.Schannel import Schannel
			self._schannel = Schannel(self._core, self._base)
		return self._schannel

	def get_count(self) -> int:
		"""[SOURce<HW>]:BB:C2K:PPARameter:TCHannel:COUNt \n
		This command sets the number of activated traffic channels. The setting takes effect only after execution of command
		method RsSmbv.Source.Bb.C2K.Pparameter.Execute.set. \n
			:return: count: integer Range: 0 to 8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:PPARameter:TCHannel:COUNt?')
		return Conversions.str_to_int(response)

	def set_count(self, count: int) -> None:
		"""[SOURce<HW>]:BB:C2K:PPARameter:TCHannel:COUNt \n
		This command sets the number of activated traffic channels. The setting takes effect only after execution of command
		method RsSmbv.Source.Bb.C2K.Pparameter.Execute.set. \n
			:param count: integer Range: 0 to 8
		"""
		param = Conversions.decimal_value_to_str(count)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:PPARameter:TCHannel:COUNt {param}')

	# noinspection PyTypeChecker
	def get_flength(self) -> enums.Cdma2KpredFramLen:
		"""[SOURce<HW>]:BB:C2K:PPARameter:TCHannel:FLENgth \n
		The command activates/deactivates the fundamental channel. The set value is specific for the selected radio configuration.
		The setting takes effect only after execution of command method RsSmbv.Source.Bb.C2K.Pparameter.Execute.set.
		It is specific for the selected radio configuration. The frame length affects the data rates that are possible within a
		channel. Changing the frame length can lead to a change of data rate and this in turn can bring about a change of Walsh
		code. \n
			:return: flength: 20| 40| 80
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:PPARameter:TCHannel:FLENgth?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KpredFramLen)

	def set_flength(self, flength: enums.Cdma2KpredFramLen) -> None:
		"""[SOURce<HW>]:BB:C2K:PPARameter:TCHannel:FLENgth \n
		The command activates/deactivates the fundamental channel. The set value is specific for the selected radio configuration.
		The setting takes effect only after execution of command method RsSmbv.Source.Bb.C2K.Pparameter.Execute.set.
		It is specific for the selected radio configuration. The frame length affects the data rates that are possible within a
		channel. Changing the frame length can lead to a change of data rate and this in turn can bring about a change of Walsh
		code. \n
			:param flength: 20| 40| 80
		"""
		param = Conversions.enum_scalar_to_str(flength, enums.Cdma2KpredFramLen)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:PPARameter:TCHannel:FLENgth {param}')
