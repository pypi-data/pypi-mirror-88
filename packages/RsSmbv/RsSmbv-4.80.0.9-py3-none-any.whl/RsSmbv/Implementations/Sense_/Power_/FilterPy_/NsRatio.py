from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NsRatio:
	"""NsRatio commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nsRatio", core, parent)

	def clone(self) -> 'NsRatio':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = NsRatio(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mtime(self):
		"""mtime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mtime'):
			from .NsRatio_.Mtime import Mtime
			self._mtime = Mtime(self._core, self._base)
		return self._mtime

	def set(self, nsratio: float, channel=repcap.Channel.Default) -> None:
		"""SENSe<CH>:[POWer]:FILTer:NSRatio \n
		Sets an upper limit for the relative noise content in fixed noise filter mode (FILTer:TYPE) . This value determines the
		proportion of intrinsic noise in the measurement results. \n
			:param nsratio: float Range: 0.001 to 1
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		param = Conversions.decimal_value_to_str(nsratio)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:FILTer:NSRatio {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""SENSe<CH>:[POWer]:FILTer:NSRatio \n
		Sets an upper limit for the relative noise content in fixed noise filter mode (FILTer:TYPE) . This value determines the
		proportion of intrinsic noise in the measurement results. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: nsratio: float Range: 0.001 to 1"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:FILTer:NSRatio?')
		return Conversions.str_to_float(response)
