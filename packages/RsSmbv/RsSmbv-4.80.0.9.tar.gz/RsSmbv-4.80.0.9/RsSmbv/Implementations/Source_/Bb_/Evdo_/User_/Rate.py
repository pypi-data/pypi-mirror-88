from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rate:
	"""Rate commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rate", core, parent)

	def clone(self) -> 'Rate':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rate(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def index(self):
		"""index commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_index'):
			from .Rate_.Index import Index
			self._index = Index(self._core, self._base)
		return self._index

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EvdoDataRate:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:RATE \n
		Queries the data rate of the packets sent to the selected user. Note: Selected rate becomes effective at the beginning of
		the next packet transmitted to the selected user. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: rate: DR4K8| DR9K6| DR19K2| DR38K4| DR76K8| DR153K6| DR307K2| DR614K4| DR921K6| DR1228K8| DR1536K| DR1843K2| DR2457K6| DR3072K| DR460K8| DR768K| DR1075K2| DR2150K4| DR3686K4| DR4300K8| DR4915K2"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:RATE?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoDataRate)
