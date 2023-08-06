from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SgDefinition:
	"""SgDefinition commands group definition. 8 total commands, 8 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sgDefinition", core, parent)

	def clone(self) -> 'SgDefinition':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SgDefinition(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def a(self):
		"""a commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_a'):
			from .SgDefinition_.A import A
			self._a = A(self._core, self._base)
		return self._a

	@property
	def b(self):
		"""b commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_b'):
			from .SgDefinition_.B import B
			self._b = B(self._core, self._base)
		return self._b

	@property
	def c(self):
		"""c commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_c'):
			from .SgDefinition_.C import C
			self._c = C(self._core, self._base)
		return self._c

	@property
	def d(self):
		"""d commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_d'):
			from .SgDefinition_.D import D
			self._d = D(self._core, self._base)
		return self._d

	@property
	def e(self):
		"""e commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_e'):
			from .SgDefinition_.E import E
			self._e = E(self._core, self._base)
		return self._e

	@property
	def f(self):
		"""f commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_f'):
			from .SgDefinition_.F import F
			self._f = F(self._core, self._base)
		return self._f

	@property
	def g(self):
		"""g commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_g'):
			from .SgDefinition_.G import G
			self._g = G(self._core, self._base)
		return self._g

	@property
	def h(self):
		"""h commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_h'):
			from .SgDefinition_.H import H
			self._h = H(self._core, self._base)
		return self._h
