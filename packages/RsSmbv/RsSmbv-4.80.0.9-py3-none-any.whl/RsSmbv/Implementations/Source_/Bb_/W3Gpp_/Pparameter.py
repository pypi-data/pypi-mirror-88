from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pparameter:
	"""Pparameter commands group definition. 7 total commands, 3 Sub-groups, 2 group commands"""

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
	def dpch(self):
		"""dpch commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dpch'):
			from .Pparameter_.Dpch import Dpch
			self._dpch = Dpch(self._core, self._base)
		return self._dpch

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Pparameter_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	@property
	def sccpch(self):
		"""sccpch commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sccpch'):
			from .Pparameter_.Sccpch import Sccpch
			self._sccpch = Sccpch(self._core, self._base)
		return self._sccpch

	# noinspection PyTypeChecker
	def get_crest(self) -> enums.CresFactMode:
		"""[SOURce<HW>]:BB:W3GPp:PPARameter:CRESt \n
		This command selects the desired range for the crest factor of the test scenario. The crest factor of the signal is kept
		in the desired range by automatically setting appropriate channelization codes and timing offsets. The setting takes
		effect only after execution of command method RsSmbv.Source.Bb.W3Gpp.Pparameter.Execute.set.
			INTRO_CMD_HELP: The settings of commands \n
			- method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Ccode.set and
			- method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Toffset.set
		Are adjusted according to the selection. \n
			:return: crest: MINimum| AVERage| WORSt MINimum The crest factor is minimized. The channelization codes are distributed uniformly over the code domain. The timing offsets are increased by 3 per channel. AVERage An average crest factor is set. The channelization codes are distributed uniformly over the code domain. The timing offsets are all set to 0. WORSt The crest factor is set to an unfavorable value (i.e. maximum) . The channelization codes are assigned in ascending order. The timing offsets are all set to 0.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:PPARameter:CRESt?')
		return Conversions.str_to_scalar_enum(response, enums.CresFactMode)

	def set_crest(self, crest: enums.CresFactMode) -> None:
		"""[SOURce<HW>]:BB:W3GPp:PPARameter:CRESt \n
		This command selects the desired range for the crest factor of the test scenario. The crest factor of the signal is kept
		in the desired range by automatically setting appropriate channelization codes and timing offsets. The setting takes
		effect only after execution of command method RsSmbv.Source.Bb.W3Gpp.Pparameter.Execute.set.
			INTRO_CMD_HELP: The settings of commands \n
			- method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Ccode.set and
			- method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Toffset.set
		Are adjusted according to the selection. \n
			:param crest: MINimum| AVERage| WORSt MINimum The crest factor is minimized. The channelization codes are distributed uniformly over the code domain. The timing offsets are increased by 3 per channel. AVERage An average crest factor is set. The channelization codes are distributed uniformly over the code domain. The timing offsets are all set to 0. WORSt The crest factor is set to an unfavorable value (i.e. maximum) . The channelization codes are assigned in ascending order. The timing offsets are all set to 0.
		"""
		param = Conversions.enum_scalar_to_str(crest, enums.CresFactMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:PPARameter:CRESt {param}')

	def get_schannels(self) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:PPARameter:SCHannels \n
		The command activates/deactivates the PCPICH, PSCH, SSCH and PCCPCH. These 'special channels' are required by a user
		equipment for synchronization. The setting takes effect only after execution of command method RsSmbv.Source.Bb.W3Gpp.
		Pparameter.Execute.set. \n
			:return: schannels: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:PPARameter:SCHannels?')
		return Conversions.str_to_bool(response)

	def set_schannels(self, schannels: bool) -> None:
		"""[SOURce<HW>]:BB:W3GPp:PPARameter:SCHannels \n
		The command activates/deactivates the PCPICH, PSCH, SSCH and PCCPCH. These 'special channels' are required by a user
		equipment for synchronization. The setting takes effect only after execution of command method RsSmbv.Source.Bb.W3Gpp.
		Pparameter.Execute.set. \n
			:param schannels: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(schannels)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:PPARameter:SCHannels {param}')
