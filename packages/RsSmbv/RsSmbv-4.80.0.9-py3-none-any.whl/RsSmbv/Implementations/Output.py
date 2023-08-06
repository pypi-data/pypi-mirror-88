from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from ..Internal.RepeatedCapability import RepeatedCapability
from .. import enums
from .. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 12 total commands, 5 Sub-groups, 2 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Output':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Output(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def afixed(self):
		"""afixed commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_afixed'):
			from .Output_.Afixed import Afixed
			self._afixed = Afixed(self._core, self._base)
		return self._afixed

	@property
	def all(self):
		"""all commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_all'):
			from .Output_.All import All
			self._all = All(self._core, self._base)
		return self._all

	@property
	def protection(self):
		"""protection commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_protection'):
			from .Output_.Protection import Protection
			self._protection = Protection(self._core, self._base)
		return self._protection

	@property
	def user(self):
		"""user commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .Output_.User import User
			self._user = User(self._core, self._base)
		return self._user

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_state'):
			from .Output_.State import State
			self._state = State(self._core, self._base)
		return self._state

	# noinspection PyTypeChecker
	def get_amode(self) -> enums.PowAttMode:
		"""OUTPut<HW>:AMODe \n
		Sets the step attenuator mode at the RF output. \n
			:return: am_ode: AUTO| FIXed AUTO The step attenuator adjusts the level settings automatically, within the full variation range. FIXed The step attenuator and amplifier stages are fixed at the current position, providing level settings with constant output VSWR. The resulting variation range is calculated according to the position.
		"""
		response = self._core.io.query_str('OUTPut<HwInstance>:AMODe?')
		return Conversions.str_to_scalar_enum(response, enums.PowAttMode)

	def set_amode(self, am_ode: enums.PowAttMode) -> None:
		"""OUTPut<HW>:AMODe \n
		Sets the step attenuator mode at the RF output. \n
			:param am_ode: AUTO| FIXed AUTO The step attenuator adjusts the level settings automatically, within the full variation range. FIXed The step attenuator and amplifier stages are fixed at the current position, providing level settings with constant output VSWR. The resulting variation range is calculated according to the position.
		"""
		param = Conversions.enum_scalar_to_str(am_ode, enums.PowAttMode)
		self._core.io.write(f'OUTPut<HwInstance>:AMODe {param}')

	# noinspection PyTypeChecker
	def get_impedance(self) -> enums.InputImpRf:
		"""OUTPut<HW>:IMPedance \n
		Queries the impedance of the RF outputs. \n
			:return: impedance: G1K| G50| G10K
		"""
		response = self._core.io.query_str('OUTPut<HwInstance>:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.InputImpRf)
