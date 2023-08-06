from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ap:
	"""Ap commands group definition. 3 total commands, 1 Sub-groups, 1 group commands
	Repeated Capability: AntennaPort, default value after init: AntennaPort.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ap", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_antennaPort_get', 'repcap_antennaPort_set', repcap.AntennaPort.Nr0)

	def clone(self) -> 'Ap':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ap(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_antennaPort_set(self, enum_value: repcap.AntennaPort) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AntennaPort.Default
		Default value after init: AntennaPort.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_antennaPort_get(self) -> repcap.AntennaPort:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def bb(self):
		"""bb commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_bb'):
			from .Ap_.Bb import Bb
			self._bb = Bb(self._core, self._base)
		return self._bb

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraBfaNtSetEmtc:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:ALLoc<CH>:PRECoding:AP \n
		Queries the used antenna ports. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: ant_ports: AP7| AP5| AP8| AP78| AP79| AP710| AP711| AP712| AP713| AP714| AP107| AP108| AP109| AP110| AP107108| AP107109"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:ALLoc{channel_cmd_val}:PRECoding:AP?')
		return Conversions.str_to_scalar_enum(response, enums.EutraBfaNtSetEmtc)
