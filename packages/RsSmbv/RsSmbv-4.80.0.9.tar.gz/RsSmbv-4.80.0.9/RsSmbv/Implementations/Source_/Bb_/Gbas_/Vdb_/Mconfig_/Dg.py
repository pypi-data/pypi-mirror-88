from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dg:
	"""Dg commands group definition. 16 total commands, 12 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dg", core, parent)

	def clone(self) -> 'Dg':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dg(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ccgp(self):
		"""ccgp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccgp'):
			from .Dg_.Ccgp import Ccgp
			self._ccgp = Ccgp(self._core, self._base)
		return self._ccgp

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_file'):
			from .Dg_.File import File
			self._file = File(self._core, self._base)
		return self._file

	@property
	def gpolynomial(self):
		"""gpolynomial commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gpolynomial'):
			from .Dg_.Gpolynomial import Gpolynomial
			self._gpolynomial = Gpolynomial(self._core, self._base)
		return self._gpolynomial

	@property
	def m11stAte(self):
		"""m11stAte commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_m11stAte'):
			from .Dg_.M11stAte import M11stAte
			self._m11stAte = M11stAte(self._core, self._base)
		return self._m11stAte

	@property
	def m1stAte(self):
		"""m1stAte commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_m1stAte'):
			from .Dg_.M1stAte import M1stAte
			self._m1stAte = M1stAte(self._core, self._base)
		return self._m1stAte

	@property
	def predefined(self):
		"""predefined commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_predefined'):
			from .Dg_.Predefined import Predefined
			self._predefined = Predefined(self._core, self._base)
		return self._predefined

	@property
	def rbOrder(self):
		"""rbOrder commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rbOrder'):
			from .Dg_.RbOrder import RbOrder
			self._rbOrder = RbOrder(self._core, self._base)
		return self._rbOrder

	@property
	def sfile(self):
		"""sfile commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfile'):
			from .Dg_.Sfile import Sfile
			self._sfile = Sfile(self._core, self._base)
		return self._sfile

	@property
	def spredefined(self):
		"""spredefined commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_spredefined'):
			from .Dg_.Spredefined import Spredefined
			self._spredefined = Spredefined(self._core, self._base)
		return self._spredefined

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Dg_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def suser(self):
		"""suser commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_suser'):
			from .Dg_.Suser import Suser
			self._suser = Suser(self._core, self._base)
		return self._suser

	@property
	def user(self):
		"""user commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .Dg_.User import User
			self._user = User(self._core, self._base)
		return self._user
