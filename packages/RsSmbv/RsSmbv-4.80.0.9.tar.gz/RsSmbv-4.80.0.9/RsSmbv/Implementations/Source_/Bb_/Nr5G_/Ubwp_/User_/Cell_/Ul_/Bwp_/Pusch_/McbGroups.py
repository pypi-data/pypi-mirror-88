from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class McbGroups:
	"""McbGroups commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcbGroups", core, parent)

	def set(self, ul_max_cbg_per_tb: enums.MaxCbgaLl, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:PUSCh:MCBGroups \n
		Limits the number of code block groups per transport block. In 5G NR a huge TB (transport block) is split into multiple
		code blocks (CB) . Multiples CBs are grouped into one code block group (CBG) . The number of code blocks grouped into the
		CBG can be limited by the 'Max Code Block Groups Per Transport Block' setting. \n
			:param ul_max_cbg_per_tb: G2| G4| DISabled| G6| G8 G2 Limits the number of code block groups per transport block to 2. G4 Limits the number of code block groups per transport block to 4. DISabled Default value, which disabled the limitation of code block groups per transport block. G6 Limits the number of code block groups per transport block to 6. G8 Limits the number of code block groups per transport block to 8.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')"""
		param = Conversions.enum_scalar_to_str(ul_max_cbg_per_tb, enums.MaxCbgaLl)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:PUSCh:MCBGroups {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default, numSuffix=repcap.NumSuffix.Default) -> enums.MaxCbgaLl:
		"""[SOURce<HW>]:BB:NR5G:UBWP:USER<CH>:CELL<ST>:UL:BWP<DIR>:PUSCh:MCBGroups \n
		Limits the number of code block groups per transport block. In 5G NR a huge TB (transport block) is split into multiple
		code blocks (CB) . Multiples CBs are grouped into one code block group (CBG) . The number of code blocks grouped into the
		CBG can be limited by the 'Max Code Block Groups Per Transport Block' setting. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param numSuffix: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Bwp')
			:return: ul_max_cbg_per_tb: G2| G4| DISabled| G6| G8 G2 Limits the number of code block groups per transport block to 2. G4 Limits the number of code block groups per transport block to 4. DISabled Default value, which disabled the limitation of code block groups per transport block. G6 Limits the number of code block groups per transport block to 6. G8 Limits the number of code block groups per transport block to 8."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		numSuffix_cmd_val = self._base.get_repcap_cmd_value(numSuffix, repcap.NumSuffix)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:UBWP:USER{channel_cmd_val}:CELL{stream_cmd_val}:UL:BWP{numSuffix_cmd_val}:PUSCh:MCBGroups?')
		return Conversions.str_to_scalar_enum(response, enums.MaxCbgaLl)
