from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sespace:
	"""Sespace commands group definition. 5 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sespace", core, parent)

	def clone(self) -> 'Sespace':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sespace(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def chk(self):
		"""chk commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_chk'):
			from .Sespace_.Chk import Chk
			self._chk = Chk(self._core, self._base)
		return self._chk

	@property
	def max(self):
		"""max commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_max'):
			from .Sespace_.Max import Max
			self._max = Max(self._core, self._base)
		return self._max

	@property
	def min(self):
		"""min commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_min'):
			from .Sespace_.Min import Min
			self._min = Min(self._core, self._base)
		return self._min

	def set(self, search_space: enums.EutraSearchSpace, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:SESPace \n
		If enabled, this parameter configures the PDCCH DCI to be transmitted within the common or UE-specific search space. \n
			:param search_space: OFF| AUTO| COMMon| UE| ON| 0| 1 COMMon|UE Common and UE-specific search spaces, as defined in the 3GPP specification OFF|AUTO For backwards compatibility only.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')"""
		param = Conversions.enum_scalar_to_str(search_space, enums.EutraSearchSpace)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:SESPace {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EutraSearchSpace:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:SESPace \n
		If enabled, this parameter configures the PDCCH DCI to be transmitted within the common or UE-specific search space. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')
			:return: search_space: OFF| AUTO| COMMon| UE| ON| 0| 1 COMMon|UE Common and UE-specific search spaces, as defined in the 3GPP specification OFF|AUTO For backwards compatibility only."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:SESPace?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSearchSpace)
