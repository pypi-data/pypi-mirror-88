from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bb:
	"""Bb commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bb", core, parent)

	def clone(self) -> 'Bb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bb(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Bb_.State import State
			self._state = State(self._core, self._base)
		return self._state

	def set(self, bbin_iq_hs_ch_bb: enums.BbDigInpBb, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BBIN:CHANnel<CH>:BB \n
		No command help available \n
			:param bbin_iq_hs_ch_bb: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(bbin_iq_hs_ch_bb, enums.BbDigInpBb)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BBIN:CHANnel{channel_cmd_val}:BB {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.BbDigInpBb:
		"""[SOURce<HW>]:BBIN:CHANnel<CH>:BB \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: bbin_iq_hs_ch_bb: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BBIN:CHANnel{channel_cmd_val}:BB?')
		return Conversions.str_to_scalar_enum(response, enums.BbDigInpBb)
