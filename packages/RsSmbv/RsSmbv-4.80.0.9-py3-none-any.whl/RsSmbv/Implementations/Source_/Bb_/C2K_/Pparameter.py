from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pparameter:
	"""Pparameter commands group definition. 12 total commands, 5 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pparameter", core, parent)

	def clone(self) -> 'Pparameter':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pparameter(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Pparameter_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def pchannel(self):
		"""pchannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pchannel'):
			from .Pparameter_.Pchannel import Pchannel
			self._pchannel = Pchannel(self._core, self._base)
		return self._pchannel

	@property
	def piChannel(self):
		"""piChannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_piChannel'):
			from .Pparameter_.PiChannel import PiChannel
			self._piChannel = PiChannel(self._core, self._base)
		return self._piChannel

	@property
	def schannel(self):
		"""schannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_schannel'):
			from .Pparameter_.Schannel import Schannel
			self._schannel = Schannel(self._core, self._base)
		return self._schannel

	@property
	def tchannel(self):
		"""tchannel commands group. 4 Sub-classes, 2 commands."""
		if not hasattr(self, '_tchannel'):
			from .Pparameter_.Tchannel import Tchannel
			self._tchannel = Tchannel(self._core, self._base)
		return self._tchannel

	# noinspection PyTypeChecker
	def get_crest(self) -> enums.CresFactMode:
		"""[SOURce<HW>]:BB:C2K:PPARameter:CRESt \n
		This command selects the desired range for the crest factor of the test scenario. The crest factor of the signal is kept
		in the desired range by automatically setting appropriate Walsh codes and timing offsets. The setting takes effect only
		after execution of command method RsSmbv.Source.Bb.C2K.Pparameter.Execute.set. The setting of command method RsSmbv.
		Source.Bb.C2K.Bstation.Cgroup.Coffset.Wcode.set is adjusted according to the selection. \n
			:return: crest: MINimum| AVERage| WORSt MINimum The crest factor is minimized. The Walsh codes are spaced as closely as possible. AVERage An average crest factor is set. The Walsh codes are distributed uniformly over the code domain. WORSt The crest factor is set to an unfavorable value (i.e. maximum) . The Walsh codes are as wildly spaced as possible.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:PPARameter:CRESt?')
		return Conversions.str_to_scalar_enum(response, enums.CresFactMode)

	def set_crest(self, crest: enums.CresFactMode) -> None:
		"""[SOURce<HW>]:BB:C2K:PPARameter:CRESt \n
		This command selects the desired range for the crest factor of the test scenario. The crest factor of the signal is kept
		in the desired range by automatically setting appropriate Walsh codes and timing offsets. The setting takes effect only
		after execution of command method RsSmbv.Source.Bb.C2K.Pparameter.Execute.set. The setting of command method RsSmbv.
		Source.Bb.C2K.Bstation.Cgroup.Coffset.Wcode.set is adjusted according to the selection. \n
			:param crest: MINimum| AVERage| WORSt MINimum The crest factor is minimized. The Walsh codes are spaced as closely as possible. AVERage An average crest factor is set. The Walsh codes are distributed uniformly over the code domain. WORSt The crest factor is set to an unfavorable value (i.e. maximum) . The Walsh codes are as wildly spaced as possible.
		"""
		param = Conversions.enum_scalar_to_str(crest, enums.CresFactMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:PPARameter:CRESt {param}')

	# noinspection PyTypeChecker
	def get_rconfiguration(self) -> enums.Cdma2KradioConf:
		"""[SOURce<HW>]:BB:C2K:PPARameter:RCONfiguration \n
		Selects the radio configuration for the traffic channel. The setting takes effect only after execution of command method
		RsSmbv.Source.Bb.C2K.Pparameter.Execute.set. \n
			:return: rconfiguration: 1| 2| 3| 4| 5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:PPARameter:RCONfiguration?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KradioConf)

	def set_rconfiguration(self, rconfiguration: enums.Cdma2KradioConf) -> None:
		"""[SOURce<HW>]:BB:C2K:PPARameter:RCONfiguration \n
		Selects the radio configuration for the traffic channel. The setting takes effect only after execution of command method
		RsSmbv.Source.Bb.C2K.Pparameter.Execute.set. \n
			:param rconfiguration: 1| 2| 3| 4| 5
		"""
		param = Conversions.enum_scalar_to_str(rconfiguration, enums.Cdma2KradioConf)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:PPARameter:RCONfiguration {param}')
