from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Xmradio:
	"""Xmradio commands group definition. 79 total commands, 5 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("xmradio", core, parent)

	def clone(self) -> 'Xmradio':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Xmradio(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_data'):
			from .Xmradio_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def satellite(self):
		"""satellite commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_satellite'):
			from .Xmradio_.Satellite import Satellite
			self._satellite = Satellite(self._core, self._base)
		return self._satellite

	@property
	def setting(self):
		"""setting commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_setting'):
			from .Xmradio_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def terrestrial(self):
		"""terrestrial commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_terrestrial'):
			from .Xmradio_.Terrestrial import Terrestrial
			self._terrestrial = Terrestrial(self._core, self._base)
		return self._terrestrial

	@property
	def trigger(self):
		"""trigger commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Xmradio_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def get_fcounter(self) -> int:
		"""[SOURce<HW>]:BB:XMRadio:FCOunter \n
		No command help available \n
			:return: fcounter: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:FCOunter?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_layer(self) -> enums.XmRadioPhysLayer:
		"""[SOURce<HW>]:BB:XMRadio:LAYer \n
		No command help available \n
			:return: layer: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:LAYer?')
		return Conversions.str_to_scalar_enum(response, enums.XmRadioPhysLayer)

	def set_layer(self, layer: enums.XmRadioPhysLayer) -> None:
		"""[SOURce<HW>]:BB:XMRadio:LAYer \n
		No command help available \n
			:param layer: No help available
		"""
		param = Conversions.enum_scalar_to_str(layer, enums.XmRadioPhysLayer)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:LAYer {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:XMRadio:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:XMRadio:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:XMRadio:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:XMRadio:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:XMRadio:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:STATe {param}')

	def get_version(self) -> str:
		"""[SOURce<HW>]:BB:XMRadio:VERSion \n
		No command help available \n
			:return: version: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:VERSion?')
		return trim_str_response(response)
