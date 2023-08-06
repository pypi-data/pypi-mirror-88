from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from ..Internal.Utilities import trim_str_response
from .. import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Test:
	"""Test commands group definition. 38 total commands, 10 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("test", core, parent)

	def clone(self) -> 'Test':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Test(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_all'):
			from .Test_.All import All
			self._all = All(self._core, self._base)
		return self._all

	@property
	def baseband(self):
		"""baseband commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_baseband'):
			from .Test_.Baseband import Baseband
			self._baseband = Baseband(self._core, self._base)
		return self._baseband

	@property
	def bb(self):
		"""bb commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_bb'):
			from .Test_.Bb import Bb
			self._bb = Bb(self._core, self._base)
		return self._bb

	@property
	def device(self):
		"""device commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_device'):
			from .Test_.Device import Device
			self._device = Device(self._core, self._base)
		return self._device

	@property
	def hs(self):
		"""hs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hs'):
			from .Test_.Hs import Hs
			self._hs = Hs(self._core, self._base)
		return self._hs

	@property
	def remote(self):
		"""remote commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_remote'):
			from .Test_.Remote import Remote
			self._remote = Remote(self._core, self._base)
		return self._remote

	@property
	def res(self):
		"""res commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_res'):
			from .Test_.Res import Res
			self._res = Res(self._core, self._base)
		return self._res

	@property
	def serror(self):
		"""serror commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_serror'):
			from .Test_.Serror import Serror
			self._serror = Serror(self._core, self._base)
		return self._serror

	@property
	def sw(self):
		"""sw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sw'):
			from .Test_.Sw import Sw
			self._sw = Sw(self._core, self._base)
		return self._sw

	@property
	def write(self):
		"""write commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_write'):
			from .Test_.Write import Write
			self._write = Write(self._core, self._base)
		return self._write

	def get_bbin(self) -> bool:
		"""TEST:BBIN \n
		No command help available \n
			:return: bbin: No help available
		"""
		response = self._core.io.query_str('TEST:BBIN?')
		return Conversions.str_to_bool(response)

	# noinspection PyTypeChecker
	def get_eiq_mode(self) -> enums.TestExtIqMode:
		"""TEST:EIQMode \n
		No command help available \n
			:return: eiq_mode: No help available
		"""
		response = self._core.io.query_str('TEST:EIQMode?')
		return Conversions.str_to_scalar_enum(response, enums.TestExtIqMode)

	def set_eiq_mode(self, eiq_mode: enums.TestExtIqMode) -> None:
		"""TEST:EIQMode \n
		No command help available \n
			:param eiq_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(eiq_mode, enums.TestExtIqMode)
		self._core.io.write(f'TEST:EIQMode {param}')

	def get_frc(self) -> str:
		"""TEST:FRC \n
		No command help available \n
			:return: test_freq_resp_cor: No help available
		"""
		response = self._core.io.query_str('TEST:FRC?')
		return trim_str_response(response)

	def set_frc(self, test_freq_resp_cor: str) -> None:
		"""TEST:FRC \n
		No command help available \n
			:param test_freq_resp_cor: No help available
		"""
		param = Conversions.value_to_quoted_str(test_freq_resp_cor)
		self._core.io.write(f'TEST:FRC {param}')

	# noinspection PyTypeChecker
	def get_level(self) -> enums.SelftLev:
		"""TEST:LEVel \n
		No command help available \n
			:return: level: No help available
		"""
		response = self._core.io.query_str('TEST:LEVel?')
		return Conversions.str_to_scalar_enum(response, enums.SelftLev)

	def set_level(self, level: enums.SelftLev) -> None:
		"""TEST:LEVel \n
		No command help available \n
			:param level: No help available
		"""
		param = Conversions.enum_scalar_to_str(level, enums.SelftLev)
		self._core.io.write(f'TEST:LEVel {param}')

	def set_nrp_trigger(self, nrp_trigger: bool) -> None:
		"""TEST:NRPTrigger \n
		No command help available \n
			:param nrp_trigger: No help available
		"""
		param = Conversions.bool_to_str(nrp_trigger)
		self._core.io.write(f'TEST:NRPTrigger {param}')

	def preset(self) -> None:
		"""TEST:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'TEST:PRESet')

	def preset_with_opc(self) -> None:
		"""TEST:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'TEST:PRESet')
