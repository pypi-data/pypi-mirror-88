from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slength:
	"""Slength commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slength", core, parent)

	def clone(self) -> 'Slength':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Slength(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def adjust(self):
		"""adjust commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adjust'):
			from .Slength_.Adjust import Adjust
			self._adjust = Adjust(self._core, self._base)
		return self._adjust

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPCCh:HS:SLENgth \n
		(Release 8 and Later) Queries the suggested and current ARB sequence length. The current ARB sequence length is adjusted
		with the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Dpcch.Hs.Slength.Adjust.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: slength: float"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPCCh:HS:SLENgth?')
		return Conversions.str_to_float(response)
