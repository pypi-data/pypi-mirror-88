from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Interleaver:
	"""Interleaver commands group definition. 1 total commands, 0 Sub-groups, 1 group commands
	Repeated Capability: Interleave, default value after init: Interleave.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("interleaver", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_interleave_get', 'repcap_interleave_set', repcap.Interleave.Nr1)

	def clone(self) -> 'Interleaver':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Interleaver(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_interleave_set(self, enum_value: repcap.Interleave) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Interleave.Default
		Default value after init: Interleave.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_interleave_get(self) -> repcap.Interleave:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	def set(self, interleaver: bool, interleave=repcap.Interleave.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:PCCPch:CCODing:INTerleaver<DI> \n
		The command activates or deactivates channel coding interleaver state 1 or 2 for the P-CCPCH. Note: The interleaver
		states do not cause the symbol rate to change. \n
			:param interleaver: ON| OFF
			:param interleave: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Interleaver')"""
		param = Conversions.bool_to_str(interleaver)
		interleave_cmd_val = self._base.get_repcap_cmd_value(interleave, repcap.Interleave)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:PCCPch:CCODing:INTerleaver{interleave_cmd_val} {param}')

	def get(self, interleave=repcap.Interleave.Default) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:PCCPch:CCODing:INTerleaver<DI> \n
		The command activates or deactivates channel coding interleaver state 1 or 2 for the P-CCPCH. Note: The interleaver
		states do not cause the symbol rate to change. \n
			:param interleave: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Interleaver')
			:return: interleaver: ON| OFF"""
		interleave_cmd_val = self._base.get_repcap_cmd_value(interleave, repcap.Interleave)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:PCCPch:CCODing:INTerleaver{interleave_cmd_val}?')
		return Conversions.str_to_bool(response)
