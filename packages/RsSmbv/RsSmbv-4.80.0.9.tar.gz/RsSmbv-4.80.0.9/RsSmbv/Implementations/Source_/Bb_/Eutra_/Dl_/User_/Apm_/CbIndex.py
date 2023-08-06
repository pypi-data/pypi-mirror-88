from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CbIndex:
	"""CbIndex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: CodeBookIx, default value after init: CodeBookIx.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cbIndex", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_codeBookIx_get', 'repcap_codeBookIx_set', repcap.CodeBookIx.Nr0)

	def clone(self) -> 'CbIndex':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = CbIndex(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_codeBookIx_set(self, enum_value: repcap.CodeBookIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to CodeBookIx.Default
		Default value after init: CodeBookIx.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_codeBookIx_get(self) -> repcap.CodeBookIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, code_book_index: int, channel=repcap.Channel.Default, codeBookIx=repcap.CodeBookIx.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:APM:CBINdex<DIR_OPTIONAL> \n
		Sets the codebook index for mapping mode Codebook. \n
			:param code_book_index: integer Range: 0 to 15
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param codeBookIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'CbIndex')"""
		param = Conversions.decimal_value_to_str(code_book_index)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeBookIx_cmd_val = self._base.get_repcap_cmd_value(codeBookIx, repcap.CodeBookIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:APM:CBINdex{codeBookIx_cmd_val} {param}')

	def get(self, channel=repcap.Channel.Default, codeBookIx=repcap.CodeBookIx.Default) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:APM:CBINdex<DIR_OPTIONAL> \n
		Sets the codebook index for mapping mode Codebook. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:param codeBookIx: optional repeated capability selector. Default value: Nr0 (settable in the interface 'CbIndex')
			:return: code_book_index: integer Range: 0 to 15"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		codeBookIx_cmd_val = self._base.get_repcap_cmd_value(codeBookIx, repcap.CodeBookIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:APM:CBINdex{codeBookIx_cmd_val}?')
		return Conversions.str_to_int(response)
