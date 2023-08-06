from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dci:
	"""Dci commands group definition. 187 total commands, 183 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dci", core, parent)

	def clone(self) -> 'Dci':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dci(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def aggLevel(self):
		"""aggLevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aggLevel'):
			from .Dci_.AggLevel import AggLevel
			self._aggLevel = AggLevel(self._core, self._base)
		return self._aggLevel

	@property
	def ai1(self):
		"""ai1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai1'):
			from .Dci_.Ai1 import Ai1
			self._ai1 = Ai1(self._core, self._base)
		return self._ai1

	@property
	def ai10(self):
		"""ai10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai10'):
			from .Dci_.Ai10 import Ai10
			self._ai10 = Ai10(self._core, self._base)
		return self._ai10

	@property
	def ai11(self):
		"""ai11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai11'):
			from .Dci_.Ai11 import Ai11
			self._ai11 = Ai11(self._core, self._base)
		return self._ai11

	@property
	def ai12(self):
		"""ai12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai12'):
			from .Dci_.Ai12 import Ai12
			self._ai12 = Ai12(self._core, self._base)
		return self._ai12

	@property
	def ai13(self):
		"""ai13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai13'):
			from .Dci_.Ai13 import Ai13
			self._ai13 = Ai13(self._core, self._base)
		return self._ai13

	@property
	def ai14(self):
		"""ai14 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai14'):
			from .Dci_.Ai14 import Ai14
			self._ai14 = Ai14(self._core, self._base)
		return self._ai14

	@property
	def ai15(self):
		"""ai15 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai15'):
			from .Dci_.Ai15 import Ai15
			self._ai15 = Ai15(self._core, self._base)
		return self._ai15

	@property
	def ai16(self):
		"""ai16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai16'):
			from .Dci_.Ai16 import Ai16
			self._ai16 = Ai16(self._core, self._base)
		return self._ai16

	@property
	def ai2(self):
		"""ai2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai2'):
			from .Dci_.Ai2 import Ai2
			self._ai2 = Ai2(self._core, self._base)
		return self._ai2

	@property
	def ai3(self):
		"""ai3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai3'):
			from .Dci_.Ai3 import Ai3
			self._ai3 = Ai3(self._core, self._base)
		return self._ai3

	@property
	def ai4(self):
		"""ai4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai4'):
			from .Dci_.Ai4 import Ai4
			self._ai4 = Ai4(self._core, self._base)
		return self._ai4

	@property
	def ai5(self):
		"""ai5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai5'):
			from .Dci_.Ai5 import Ai5
			self._ai5 = Ai5(self._core, self._base)
		return self._ai5

	@property
	def ai6(self):
		"""ai6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai6'):
			from .Dci_.Ai6 import Ai6
			self._ai6 = Ai6(self._core, self._base)
		return self._ai6

	@property
	def ai7(self):
		"""ai7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai7'):
			from .Dci_.Ai7 import Ai7
			self._ai7 = Ai7(self._core, self._base)
		return self._ai7

	@property
	def ai8(self):
		"""ai8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai8'):
			from .Dci_.Ai8 import Ai8
			self._ai8 = Ai8(self._core, self._base)
		return self._ai8

	@property
	def ai9(self):
		"""ai9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ai9'):
			from .Dci_.Ai9 import Ai9
			self._ai9 = Ai9(self._core, self._base)
		return self._ai9

	@property
	def antPorts(self):
		"""antPorts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_antPorts'):
			from .Dci_.AntPorts import AntPorts
			self._antPorts = AntPorts(self._core, self._base)
		return self._antPorts

	@property
	def bitLength(self):
		"""bitLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitLength'):
			from .Dci_.BitLength import BitLength
			self._bitLength = BitLength(self._core, self._base)
		return self._bitLength

	@property
	def boind(self):
		"""boind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_boind'):
			from .Dci_.Boind import Boind
			self._boind = Boind(self._core, self._base)
		return self._boind

	@property
	def bwind(self):
		"""bwind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bwind'):
			from .Dci_.Bwind import Bwind
			self._bwind = Bwind(self._core, self._base)
		return self._bwind

	@property
	def caind(self):
		"""caind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_caind'):
			from .Dci_.Caind import Caind
			self._caind = Caind(self._core, self._base)
		return self._caind

	@property
	def candidate(self):
		"""candidate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_candidate'):
			from .Dci_.Candidate import Candidate
			self._candidate = Candidate(self._core, self._base)
		return self._candidate

	@property
	def cbgfi(self):
		"""cbgfi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbgfi'):
			from .Dci_.Cbgfi import Cbgfi
			self._cbgfi = Cbgfi(self._core, self._base)
		return self._cbgfi

	@property
	def cbgti(self):
		"""cbgti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbgti'):
			from .Dci_.Cbgti import Cbgti
			self._cbgti = Cbgti(self._core, self._base)
		return self._cbgti

	@property
	def ci10(self):
		"""ci10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci10'):
			from .Dci_.Ci10 import Ci10
			self._ci10 = Ci10(self._core, self._base)
		return self._ci10

	@property
	def ci11(self):
		"""ci11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci11'):
			from .Dci_.Ci11 import Ci11
			self._ci11 = Ci11(self._core, self._base)
		return self._ci11

	@property
	def ci12(self):
		"""ci12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci12'):
			from .Dci_.Ci12 import Ci12
			self._ci12 = Ci12(self._core, self._base)
		return self._ci12

	@property
	def ci13(self):
		"""ci13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci13'):
			from .Dci_.Ci13 import Ci13
			self._ci13 = Ci13(self._core, self._base)
		return self._ci13

	@property
	def ci14(self):
		"""ci14 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci14'):
			from .Dci_.Ci14 import Ci14
			self._ci14 = Ci14(self._core, self._base)
		return self._ci14

	@property
	def ci15(self):
		"""ci15 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci15'):
			from .Dci_.Ci15 import Ci15
			self._ci15 = Ci15(self._core, self._base)
		return self._ci15

	@property
	def ci16(self):
		"""ci16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci16'):
			from .Dci_.Ci16 import Ci16
			self._ci16 = Ci16(self._core, self._base)
		return self._ci16

	@property
	def ci2(self):
		"""ci2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci2'):
			from .Dci_.Ci2 import Ci2
			self._ci2 = Ci2(self._core, self._base)
		return self._ci2

	@property
	def ci3(self):
		"""ci3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci3'):
			from .Dci_.Ci3 import Ci3
			self._ci3 = Ci3(self._core, self._base)
		return self._ci3

	@property
	def ci4(self):
		"""ci4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci4'):
			from .Dci_.Ci4 import Ci4
			self._ci4 = Ci4(self._core, self._base)
		return self._ci4

	@property
	def ci5(self):
		"""ci5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci5'):
			from .Dci_.Ci5 import Ci5
			self._ci5 = Ci5(self._core, self._base)
		return self._ci5

	@property
	def ci6(self):
		"""ci6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci6'):
			from .Dci_.Ci6 import Ci6
			self._ci6 = Ci6(self._core, self._base)
		return self._ci6

	@property
	def ci7(self):
		"""ci7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci7'):
			from .Dci_.Ci7 import Ci7
			self._ci7 = Ci7(self._core, self._base)
		return self._ci7

	@property
	def ci8(self):
		"""ci8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci8'):
			from .Dci_.Ci8 import Ci8
			self._ci8 = Ci8(self._core, self._base)
		return self._ci8

	@property
	def ci9(self):
		"""ci9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ci9'):
			from .Dci_.Ci9 import Ci9
			self._ci9 = Ci9(self._core, self._base)
		return self._ci9

	@property
	def cl1(self):
		"""cl1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl1'):
			from .Dci_.Cl1 import Cl1
			self._cl1 = Cl1(self._core, self._base)
		return self._cl1

	@property
	def cl10(self):
		"""cl10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl10'):
			from .Dci_.Cl10 import Cl10
			self._cl10 = Cl10(self._core, self._base)
		return self._cl10

	@property
	def cl11(self):
		"""cl11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl11'):
			from .Dci_.Cl11 import Cl11
			self._cl11 = Cl11(self._core, self._base)
		return self._cl11

	@property
	def cl12(self):
		"""cl12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl12'):
			from .Dci_.Cl12 import Cl12
			self._cl12 = Cl12(self._core, self._base)
		return self._cl12

	@property
	def cl13(self):
		"""cl13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl13'):
			from .Dci_.Cl13 import Cl13
			self._cl13 = Cl13(self._core, self._base)
		return self._cl13

	@property
	def cl14(self):
		"""cl14 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl14'):
			from .Dci_.Cl14 import Cl14
			self._cl14 = Cl14(self._core, self._base)
		return self._cl14

	@property
	def cl15(self):
		"""cl15 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl15'):
			from .Dci_.Cl15 import Cl15
			self._cl15 = Cl15(self._core, self._base)
		return self._cl15

	@property
	def cl16(self):
		"""cl16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl16'):
			from .Dci_.Cl16 import Cl16
			self._cl16 = Cl16(self._core, self._base)
		return self._cl16

	@property
	def cl17(self):
		"""cl17 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl17'):
			from .Dci_.Cl17 import Cl17
			self._cl17 = Cl17(self._core, self._base)
		return self._cl17

	@property
	def cl18(self):
		"""cl18 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl18'):
			from .Dci_.Cl18 import Cl18
			self._cl18 = Cl18(self._core, self._base)
		return self._cl18

	@property
	def cl19(self):
		"""cl19 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl19'):
			from .Dci_.Cl19 import Cl19
			self._cl19 = Cl19(self._core, self._base)
		return self._cl19

	@property
	def cl2(self):
		"""cl2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl2'):
			from .Dci_.Cl2 import Cl2
			self._cl2 = Cl2(self._core, self._base)
		return self._cl2

	@property
	def cl20(self):
		"""cl20 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl20'):
			from .Dci_.Cl20 import Cl20
			self._cl20 = Cl20(self._core, self._base)
		return self._cl20

	@property
	def cl21(self):
		"""cl21 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl21'):
			from .Dci_.Cl21 import Cl21
			self._cl21 = Cl21(self._core, self._base)
		return self._cl21

	@property
	def cl22(self):
		"""cl22 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl22'):
			from .Dci_.Cl22 import Cl22
			self._cl22 = Cl22(self._core, self._base)
		return self._cl22

	@property
	def cl3(self):
		"""cl3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl3'):
			from .Dci_.Cl3 import Cl3
			self._cl3 = Cl3(self._core, self._base)
		return self._cl3

	@property
	def cl4(self):
		"""cl4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl4'):
			from .Dci_.Cl4 import Cl4
			self._cl4 = Cl4(self._core, self._base)
		return self._cl4

	@property
	def cl5(self):
		"""cl5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl5'):
			from .Dci_.Cl5 import Cl5
			self._cl5 = Cl5(self._core, self._base)
		return self._cl5

	@property
	def cl6(self):
		"""cl6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl6'):
			from .Dci_.Cl6 import Cl6
			self._cl6 = Cl6(self._core, self._base)
		return self._cl6

	@property
	def cl7(self):
		"""cl7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl7'):
			from .Dci_.Cl7 import Cl7
			self._cl7 = Cl7(self._core, self._base)
		return self._cl7

	@property
	def cl8(self):
		"""cl8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl8'):
			from .Dci_.Cl8 import Cl8
			self._cl8 = Cl8(self._core, self._base)
		return self._cl8

	@property
	def cl9(self):
		"""cl9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cl9'):
			from .Dci_.Cl9 import Cl9
			self._cl9 = Cl9(self._core, self._base)
		return self._cl9

	@property
	def cpdsch(self):
		"""cpdsch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpdsch'):
			from .Dci_.Cpdsch import Cpdsch
			self._cpdsch = Cpdsch(self._core, self._base)
		return self._cpdsch

	@property
	def csiRequest(self):
		"""csiRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csiRequest'):
			from .Dci_.CsiRequest import CsiRequest
			self._csiRequest = CsiRequest(self._core, self._base)
		return self._csiRequest

	@property
	def dai1(self):
		"""dai1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dai1'):
			from .Dci_.Dai1 import Dai1
			self._dai1 = Dai1(self._core, self._base)
		return self._dai1

	@property
	def dai2(self):
		"""dai2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dai2'):
			from .Dci_.Dai2 import Dai2
			self._dai2 = Dai2(self._core, self._base)
		return self._dai2

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Dci_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def di1(self):
		"""di1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di1'):
			from .Dci_.Di1 import Di1
			self._di1 = Di1(self._core, self._base)
		return self._di1

	@property
	def di10(self):
		"""di10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di10'):
			from .Dci_.Di10 import Di10
			self._di10 = Di10(self._core, self._base)
		return self._di10

	@property
	def di2(self):
		"""di2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di2'):
			from .Dci_.Di2 import Di2
			self._di2 = Di2(self._core, self._base)
		return self._di2

	@property
	def di3(self):
		"""di3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di3'):
			from .Dci_.Di3 import Di3
			self._di3 = Di3(self._core, self._base)
		return self._di3

	@property
	def di4(self):
		"""di4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di4'):
			from .Dci_.Di4 import Di4
			self._di4 = Di4(self._core, self._base)
		return self._di4

	@property
	def di5(self):
		"""di5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di5'):
			from .Dci_.Di5 import Di5
			self._di5 = Di5(self._core, self._base)
		return self._di5

	@property
	def di6(self):
		"""di6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di6'):
			from .Dci_.Di6 import Di6
			self._di6 = Di6(self._core, self._base)
		return self._di6

	@property
	def di7(self):
		"""di7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di7'):
			from .Dci_.Di7 import Di7
			self._di7 = Di7(self._core, self._base)
		return self._di7

	@property
	def di8(self):
		"""di8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di8'):
			from .Dci_.Di8 import Di8
			self._di8 = Di8(self._core, self._base)
		return self._di8

	@property
	def di9(self):
		"""di9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_di9'):
			from .Dci_.Di9 import Di9
			self._di9 = Di9(self._core, self._base)
		return self._di9

	@property
	def dlist(self):
		"""dlist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlist'):
			from .Dci_.Dlist import Dlist
			self._dlist = Dlist(self._core, self._base)
		return self._dlist

	@property
	def dmsqInit(self):
		"""dmsqInit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmsqInit'):
			from .Dci_.DmsqInit import DmsqInit
			self._dmsqInit = DmsqInit(self._core, self._base)
		return self._dmsqInit

	@property
	def fmt(self):
		"""fmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmt'):
			from .Dci_.Fmt import Fmt
			self._fmt = Fmt(self._core, self._base)
		return self._fmt

	@property
	def frdRes(self):
		"""frdRes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frdRes'):
			from .Dci_.FrdRes import FrdRes
			self._frdRes = FrdRes(self._core, self._base)
		return self._frdRes

	@property
	def frhFlag(self):
		"""frhFlag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frhFlag'):
			from .Dci_.FrhFlag import FrhFlag
			self._frhFlag = FrhFlag(self._core, self._base)
		return self._frhFlag

	@property
	def haproc(self):
		"""haproc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_haproc'):
			from .Dci_.Haproc import Haproc
			self._haproc = Haproc(self._core, self._base)
		return self._haproc

	@property
	def identifier(self):
		"""identifier commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_identifier'):
			from .Dci_.Identifier import Identifier
			self._identifier = Identifier(self._core, self._base)
		return self._identifier

	@property
	def index(self):
		"""index commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_index'):
			from .Dci_.Index import Index
			self._index = Index(self._core, self._base)
		return self._index

	@property
	def initPattern(self):
		"""initPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_initPattern'):
			from .Dci_.InitPattern import InitPattern
			self._initPattern = InitPattern(self._core, self._base)
		return self._initPattern

	@property
	def moffs(self):
		"""moffs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_moffs'):
			from .Dci_.Moffs import Moffs
			self._moffs = Moffs(self._core, self._base)
		return self._moffs

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Dci_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def pdsharq(self):
		"""pdsharq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdsharq'):
			from .Dci_.Pdsharq import Pdsharq
			self._pdsharq = Pdsharq(self._core, self._base)
		return self._pdsharq

	@property
	def pe1(self):
		"""pe1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe1'):
			from .Dci_.Pe1 import Pe1
			self._pe1 = Pe1(self._core, self._base)
		return self._pe1

	@property
	def pe2(self):
		"""pe2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe2'):
			from .Dci_.Pe2 import Pe2
			self._pe2 = Pe2(self._core, self._base)
		return self._pe2

	@property
	def pe3(self):
		"""pe3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe3'):
			from .Dci_.Pe3 import Pe3
			self._pe3 = Pe3(self._core, self._base)
		return self._pe3

	@property
	def pe4(self):
		"""pe4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe4'):
			from .Dci_.Pe4 import Pe4
			self._pe4 = Pe4(self._core, self._base)
		return self._pe4

	@property
	def pe5(self):
		"""pe5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe5'):
			from .Dci_.Pe5 import Pe5
			self._pe5 = Pe5(self._core, self._base)
		return self._pe5

	@property
	def pe6(self):
		"""pe6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe6'):
			from .Dci_.Pe6 import Pe6
			self._pe6 = Pe6(self._core, self._base)
		return self._pe6

	@property
	def pe7(self):
		"""pe7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe7'):
			from .Dci_.Pe7 import Pe7
			self._pe7 = Pe7(self._core, self._base)
		return self._pe7

	@property
	def pe8(self):
		"""pe8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe8'):
			from .Dci_.Pe8 import Pe8
			self._pe8 = Pe8(self._core, self._base)
		return self._pe8

	@property
	def pe9(self):
		"""pe9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pe9'):
			from .Dci_.Pe9 import Pe9
			self._pe9 = Pe9(self._core, self._base)
		return self._pe9

	@property
	def prbBundling(self):
		"""prbBundling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbBundling'):
			from .Dci_.PrbBundling import PrbBundling
			self._prbBundling = PrbBundling(self._core, self._base)
		return self._prbBundling

	@property
	def precInfo(self):
		"""precInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_precInfo'):
			from .Dci_.PrecInfo import PrecInfo
			self._precInfo = PrecInfo(self._core, self._base)
		return self._precInfo

	@property
	def ptdmrs(self):
		"""ptdmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptdmrs'):
			from .Dci_.Ptdmrs import Ptdmrs
			self._ptdmrs = Ptdmrs(self._core, self._base)
		return self._ptdmrs

	@property
	def pucresInd(self):
		"""pucresInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pucresInd'):
			from .Dci_.PucresInd import PucresInd
			self._pucresInd = PucresInd(self._core, self._base)
		return self._pucresInd

	@property
	def resved(self):
		"""resved commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_resved'):
			from .Dci_.Resved import Resved
			self._resved = Resved(self._core, self._base)
		return self._resved

	@property
	def rmind(self):
		"""rmind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmind'):
			from .Dci_.Rmind import Rmind
			self._rmind = Rmind(self._core, self._base)
		return self._rmind

	@property
	def rnti(self):
		"""rnti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rnti'):
			from .Dci_.Rnti import Rnti
			self._rnti = Rnti(self._core, self._base)
		return self._rnti

	@property
	def si1(self):
		"""si1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si1'):
			from .Dci_.Si1 import Si1
			self._si1 = Si1(self._core, self._base)
		return self._si1

	@property
	def si10(self):
		"""si10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si10'):
			from .Dci_.Si10 import Si10
			self._si10 = Si10(self._core, self._base)
		return self._si10

	@property
	def si11(self):
		"""si11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si11'):
			from .Dci_.Si11 import Si11
			self._si11 = Si11(self._core, self._base)
		return self._si11

	@property
	def si12(self):
		"""si12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si12'):
			from .Dci_.Si12 import Si12
			self._si12 = Si12(self._core, self._base)
		return self._si12

	@property
	def si13(self):
		"""si13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si13'):
			from .Dci_.Si13 import Si13
			self._si13 = Si13(self._core, self._base)
		return self._si13

	@property
	def si14(self):
		"""si14 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si14'):
			from .Dci_.Si14 import Si14
			self._si14 = Si14(self._core, self._base)
		return self._si14

	@property
	def si15(self):
		"""si15 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si15'):
			from .Dci_.Si15 import Si15
			self._si15 = Si15(self._core, self._base)
		return self._si15

	@property
	def si16(self):
		"""si16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si16'):
			from .Dci_.Si16 import Si16
			self._si16 = Si16(self._core, self._base)
		return self._si16

	@property
	def si2(self):
		"""si2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si2'):
			from .Dci_.Si2 import Si2
			self._si2 = Si2(self._core, self._base)
		return self._si2

	@property
	def si3(self):
		"""si3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si3'):
			from .Dci_.Si3 import Si3
			self._si3 = Si3(self._core, self._base)
		return self._si3

	@property
	def si4(self):
		"""si4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si4'):
			from .Dci_.Si4 import Si4
			self._si4 = Si4(self._core, self._base)
		return self._si4

	@property
	def si5(self):
		"""si5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si5'):
			from .Dci_.Si5 import Si5
			self._si5 = Si5(self._core, self._base)
		return self._si5

	@property
	def si6(self):
		"""si6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si6'):
			from .Dci_.Si6 import Si6
			self._si6 = Si6(self._core, self._base)
		return self._si6

	@property
	def si7(self):
		"""si7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si7'):
			from .Dci_.Si7 import Si7
			self._si7 = Si7(self._core, self._base)
		return self._si7

	@property
	def si8(self):
		"""si8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si8'):
			from .Dci_.Si8 import Si8
			self._si8 = Si8(self._core, self._base)
		return self._si8

	@property
	def si9(self):
		"""si9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_si9'):
			from .Dci_.Si9 import Si9
			self._si9 = Si9(self._core, self._base)
		return self._si9

	@property
	def siInd(self):
		"""siInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_siInd'):
			from .Dci_.SiInd import SiInd
			self._siInd = SiInd(self._core, self._base)
		return self._siInd

	@property
	def smind(self):
		"""smind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smind'):
			from .Dci_.Smind import Smind
			self._smind = Smind(self._core, self._base)
		return self._smind

	@property
	def smsgs(self):
		"""smsgs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smsgs'):
			from .Dci_.Smsgs import Smsgs
			self._smsgs = Smsgs(self._core, self._base)
		return self._smsgs

	@property
	def sr1(self):
		"""sr1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr1'):
			from .Dci_.Sr1 import Sr1
			self._sr1 = Sr1(self._core, self._base)
		return self._sr1

	@property
	def sr10(self):
		"""sr10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr10'):
			from .Dci_.Sr10 import Sr10
			self._sr10 = Sr10(self._core, self._base)
		return self._sr10

	@property
	def sr11(self):
		"""sr11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr11'):
			from .Dci_.Sr11 import Sr11
			self._sr11 = Sr11(self._core, self._base)
		return self._sr11

	@property
	def sr2(self):
		"""sr2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr2'):
			from .Dci_.Sr2 import Sr2
			self._sr2 = Sr2(self._core, self._base)
		return self._sr2

	@property
	def sr3(self):
		"""sr3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr3'):
			from .Dci_.Sr3 import Sr3
			self._sr3 = Sr3(self._core, self._base)
		return self._sr3

	@property
	def sr4(self):
		"""sr4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr4'):
			from .Dci_.Sr4 import Sr4
			self._sr4 = Sr4(self._core, self._base)
		return self._sr4

	@property
	def sr5(self):
		"""sr5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr5'):
			from .Dci_.Sr5 import Sr5
			self._sr5 = Sr5(self._core, self._base)
		return self._sr5

	@property
	def sr6(self):
		"""sr6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr6'):
			from .Dci_.Sr6 import Sr6
			self._sr6 = Sr6(self._core, self._base)
		return self._sr6

	@property
	def sr7(self):
		"""sr7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr7'):
			from .Dci_.Sr7 import Sr7
			self._sr7 = Sr7(self._core, self._base)
		return self._sr7

	@property
	def sr8(self):
		"""sr8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr8'):
			from .Dci_.Sr8 import Sr8
			self._sr8 = Sr8(self._core, self._base)
		return self._sr8

	@property
	def sr9(self):
		"""sr9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sr9'):
			from .Dci_.Sr9 import Sr9
			self._sr9 = Sr9(self._core, self._base)
		return self._sr9

	@property
	def srsRequest(self):
		"""srsRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srsRequest'):
			from .Dci_.SrsRequest import SrsRequest
			self._srsRequest = SrsRequest(self._core, self._base)
		return self._srsRequest

	@property
	def srsResInd(self):
		"""srsResInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srsResInd'):
			from .Dci_.SrsResInd import SrsResInd
			self._srsResInd = SrsResInd(self._core, self._base)
		return self._srsResInd

	@property
	def ssp(self):
		"""ssp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssp'):
			from .Dci_.Ssp import Ssp
			self._ssp = Ssp(self._core, self._base)
		return self._ssp

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Dci_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tb1(self):
		"""tb1 commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tb1'):
			from .Dci_.Tb1 import Tb1
			self._tb1 = Tb1(self._core, self._base)
		return self._tb1

	@property
	def tb2(self):
		"""tb2 commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tb2'):
			from .Dci_.Tb2 import Tb2
			self._tb2 = Tb2(self._core, self._base)
		return self._tb2

	@property
	def tbScaling(self):
		"""tbScaling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbScaling'):
			from .Dci_.TbScaling import TbScaling
			self._tbScaling = TbScaling(self._core, self._base)
		return self._tbScaling

	@property
	def tci(self):
		"""tci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tci'):
			from .Dci_.Tci import Tci
			self._tci = Tci(self._core, self._base)
		return self._tci

	@property
	def tidRes(self):
		"""tidRes commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tidRes'):
			from .Dci_.TidRes import TidRes
			self._tidRes = TidRes(self._core, self._base)
		return self._tidRes

	@property
	def tp1(self):
		"""tp1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp1'):
			from .Dci_.Tp1 import Tp1
			self._tp1 = Tp1(self._core, self._base)
		return self._tp1

	@property
	def tp10(self):
		"""tp10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp10'):
			from .Dci_.Tp10 import Tp10
			self._tp10 = Tp10(self._core, self._base)
		return self._tp10

	@property
	def tp11(self):
		"""tp11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp11'):
			from .Dci_.Tp11 import Tp11
			self._tp11 = Tp11(self._core, self._base)
		return self._tp11

	@property
	def tp12(self):
		"""tp12 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp12'):
			from .Dci_.Tp12 import Tp12
			self._tp12 = Tp12(self._core, self._base)
		return self._tp12

	@property
	def tp13(self):
		"""tp13 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp13'):
			from .Dci_.Tp13 import Tp13
			self._tp13 = Tp13(self._core, self._base)
		return self._tp13

	@property
	def tp14(self):
		"""tp14 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp14'):
			from .Dci_.Tp14 import Tp14
			self._tp14 = Tp14(self._core, self._base)
		return self._tp14

	@property
	def tp15(self):
		"""tp15 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp15'):
			from .Dci_.Tp15 import Tp15
			self._tp15 = Tp15(self._core, self._base)
		return self._tp15

	@property
	def tp16(self):
		"""tp16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp16'):
			from .Dci_.Tp16 import Tp16
			self._tp16 = Tp16(self._core, self._base)
		return self._tp16

	@property
	def tp17(self):
		"""tp17 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp17'):
			from .Dci_.Tp17 import Tp17
			self._tp17 = Tp17(self._core, self._base)
		return self._tp17

	@property
	def tp18(self):
		"""tp18 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp18'):
			from .Dci_.Tp18 import Tp18
			self._tp18 = Tp18(self._core, self._base)
		return self._tp18

	@property
	def tp19(self):
		"""tp19 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp19'):
			from .Dci_.Tp19 import Tp19
			self._tp19 = Tp19(self._core, self._base)
		return self._tp19

	@property
	def tp2(self):
		"""tp2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp2'):
			from .Dci_.Tp2 import Tp2
			self._tp2 = Tp2(self._core, self._base)
		return self._tp2

	@property
	def tp20(self):
		"""tp20 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp20'):
			from .Dci_.Tp20 import Tp20
			self._tp20 = Tp20(self._core, self._base)
		return self._tp20

	@property
	def tp21(self):
		"""tp21 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp21'):
			from .Dci_.Tp21 import Tp21
			self._tp21 = Tp21(self._core, self._base)
		return self._tp21

	@property
	def tp22(self):
		"""tp22 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp22'):
			from .Dci_.Tp22 import Tp22
			self._tp22 = Tp22(self._core, self._base)
		return self._tp22

	@property
	def tp3(self):
		"""tp3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp3'):
			from .Dci_.Tp3 import Tp3
			self._tp3 = Tp3(self._core, self._base)
		return self._tp3

	@property
	def tp4(self):
		"""tp4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp4'):
			from .Dci_.Tp4 import Tp4
			self._tp4 = Tp4(self._core, self._base)
		return self._tp4

	@property
	def tp5(self):
		"""tp5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp5'):
			from .Dci_.Tp5 import Tp5
			self._tp5 = Tp5(self._core, self._base)
		return self._tp5

	@property
	def tp6(self):
		"""tp6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp6'):
			from .Dci_.Tp6 import Tp6
			self._tp6 = Tp6(self._core, self._base)
		return self._tp6

	@property
	def tp7(self):
		"""tp7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp7'):
			from .Dci_.Tp7 import Tp7
			self._tp7 = Tp7(self._core, self._base)
		return self._tp7

	@property
	def tp8(self):
		"""tp8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp8'):
			from .Dci_.Tp8 import Tp8
			self._tp8 = Tp8(self._core, self._base)
		return self._tp8

	@property
	def tp9(self):
		"""tp9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp9'):
			from .Dci_.Tp9 import Tp9
			self._tp9 = Tp9(self._core, self._base)
		return self._tp9

	@property
	def tpucch(self):
		"""tpucch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpucch'):
			from .Dci_.Tpucch import Tpucch
			self._tpucch = Tpucch(self._core, self._base)
		return self._tpucch

	@property
	def tpusch(self):
		"""tpusch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpusch'):
			from .Dci_.Tpusch import Tpusch
			self._tpusch = Tpusch(self._core, self._base)
		return self._tpusch

	@property
	def ulSchInd(self):
		"""ulSchInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulSchInd'):
			from .Dci_.UlSchInd import UlSchInd
			self._ulSchInd = UlSchInd(self._core, self._base)
		return self._ulSchInd

	@property
	def usage(self):
		"""usage commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_usage'):
			from .Dci_.Usage import Usage
			self._usage = Usage(self._core, self._base)
		return self._usage

	@property
	def usInd(self):
		"""usInd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_usInd'):
			from .Dci_.UsInd import UsInd
			self._usInd = UsInd(self._core, self._base)
		return self._usInd

	@property
	def vtprb(self):
		"""vtprb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vtprb'):
			from .Dci_.Vtprb import Vtprb
			self._vtprb = Vtprb(self._core, self._base)
		return self._vtprb

	@property
	def wa1(self):
		"""wa1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa1'):
			from .Dci_.Wa1 import Wa1
			self._wa1 = Wa1(self._core, self._base)
		return self._wa1

	@property
	def wa10(self):
		"""wa10 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa10'):
			from .Dci_.Wa10 import Wa10
			self._wa10 = Wa10(self._core, self._base)
		return self._wa10

	@property
	def wa2(self):
		"""wa2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa2'):
			from .Dci_.Wa2 import Wa2
			self._wa2 = Wa2(self._core, self._base)
		return self._wa2

	@property
	def wa3(self):
		"""wa3 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa3'):
			from .Dci_.Wa3 import Wa3
			self._wa3 = Wa3(self._core, self._base)
		return self._wa3

	@property
	def wa4(self):
		"""wa4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa4'):
			from .Dci_.Wa4 import Wa4
			self._wa4 = Wa4(self._core, self._base)
		return self._wa4

	@property
	def wa5(self):
		"""wa5 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa5'):
			from .Dci_.Wa5 import Wa5
			self._wa5 = Wa5(self._core, self._base)
		return self._wa5

	@property
	def wa6(self):
		"""wa6 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa6'):
			from .Dci_.Wa6 import Wa6
			self._wa6 = Wa6(self._core, self._base)
		return self._wa6

	@property
	def wa7(self):
		"""wa7 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa7'):
			from .Dci_.Wa7 import Wa7
			self._wa7 = Wa7(self._core, self._base)
		return self._wa7

	@property
	def wa8(self):
		"""wa8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa8'):
			from .Dci_.Wa8 import Wa8
			self._wa8 = Wa8(self._core, self._base)
		return self._wa8

	@property
	def wa9(self):
		"""wa9 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wa9'):
			from .Dci_.Wa9 import Wa9
			self._wa9 = Wa9(self._core, self._base)
		return self._wa9

	@property
	def zcrTrigg(self):
		"""zcrTrigg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zcrTrigg'):
			from .Dci_.ZcrTrigg import ZcrTrigg
			self._zcrTrigg = ZcrTrigg(self._core, self._base)
		return self._zcrTrigg
