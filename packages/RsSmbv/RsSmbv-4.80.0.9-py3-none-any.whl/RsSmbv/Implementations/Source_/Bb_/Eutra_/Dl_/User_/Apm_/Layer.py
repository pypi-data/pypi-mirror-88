from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Layer:
	"""Layer commands group definition. 2 total commands, 1 Sub-groups, 0 group commands
	Repeated Capability: Layer, default value after init: Layer.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("layer", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_layer_get', 'repcap_layer_set', repcap.Layer.Nr0)

	def clone(self) -> 'Layer':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Layer(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_layer_set(self, enum_value: repcap.Layer) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Layer.Default
		Default value after init: Layer.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_layer_get(self) -> repcap.Layer:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def ap(self):
		"""ap commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ap'):
			from .Layer_.Ap import Ap
			self._ap = Ap(self._core, self._base)
		return self._ap
