#
# Copyright and User License
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright Vasilis.Vlachoudis@cern.ch for the
# European Organization for Nuclear Research (CERN)
#
# Please consult the flair documentation for the license
#
# DISCLAIMER
# ~~~~~~~~~~
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, IMPLIED WARRANTIES OF MERCHANTABILITY, OF
# SATISFACTORY QUALITY, AND FITNESS FOR A PARTICULAR PURPOSE
# OR USE ARE DISCLAIMED. THE COPYRIGHT HOLDERS AND THE
# AUTHORS MAKE NO REPRESENTATION THAT THE SOFTWARE AND
# MODIFICATIONS THEREOF, WILL NOT INFRINGE ANY PATENT,
# COPYRIGHT, TRADE SECRET OR OTHER PROPRIETARY RIGHT.
#
# LIMITATION OF LIABILITY
# ~~~~~~~~~~~~~~~~~~~~~~~
# THE COPYRIGHT HOLDERS AND THE AUTHORS SHALL HAVE NO
# LIABILITY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL,
# CONSEQUENTIAL, EXEMPLARY, OR PUNITIVE DAMAGES OF ANY
# CHARACTER INCLUDING, WITHOUT LIMITATION, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES, LOSS OF USE, DATA OR PROFITS,
# OR BUSINESS INTERRUPTION, HOWEVER CAUSED AND ON ANY THEORY
# OF CONTRACT, WARRANTY, TORT (INCLUDING NEGLIGENCE), PRODUCT
# LIABILITY OR OTHERWISE, ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
# $Log: csg.py,v $
# Revision 1.16  2011/05/20 13:05:40  bnv
# Heavy modifications for OutputMessages
# Validation of Input
# Include assert statements in card.ini
# Better messages
# CardWidget: validation -> updateStatus
#
# Revision 1.15  2011/02/03 07:58:09  bnv
# Python3: Changed <> to !=
# Python3: Corrected mixed tabs and spaces indentation
#
# Revision 1.14  2011/02/02 17:11:18  bnv
# Corrected continuation REGION cards in Mcnp and Povray
#
# Revision 1.13  2010/11/06 10:44:39  bnv
# RunFrame corrected for multiple selection
# Timeout doesn't erase last stats
# Export to image added in geoviewer
#
# Revision 1.12  2010/10/08 14:24:34  bnv
# Corrections from pychecker
#
# Revision 1.11  2010/09/28 07:08:21  bnv
# Highlighting search in InputFrame
# GeometryViewer interface corrections + additions of errors
#
# Revision 1.10  2010/03/12 13:52:55  bnv
# Release: 0.8.0
#
# Revision 1.9  2010/02/23 10:34:21  bnv
# Correction in error checking of REGION
#
# Revision 1.8  2010/02/11 08:29:15  bnv
# Added: Balloon help for the InputFrame
# Bug fixing for various conditions where nothing is activated
#
# Revision 1.7  2009/11/09 16:46:18  bnv
# FileDialog addition
#
# Revision 1.6  2008/04/30 15:00:35  bnv
# Changed range to range to relax memory allocations
#
# Revision 1.5  2008/04/25 16:16:35  bnv
# Simple REGION checking for the correctness of the expression
#
# Revision 1.4  2008/03/27 16:39:32  bnv
# License modified
# Several small bugs especially in the use of FREE format for plotting geometries
#
# Revision 1.3  2007/02/07 11:07:56  bnv
# Working on documentation
#
# Revision 1.2  2006/11/20 13:16:27  bnv
# Licence Added in all files
#
# Revision 1.1  2006/09/29 15:16:32  bnv
# *** empty log message ***
#
# Author:	Vasilis.Vlachoudis@cern.ch
# Date:	18-May-2004

__author__ = "Vasilis Vlachoudis"
__email__  = "Vasilis.Vlachoudis@cern.ch"

class CSGException(Exception):
	pass

MAXEXPR = 10000

# ----------------------------------------------------------------------
def tokenize(expr):
	"""return a list of expression tokens"""
	lst = []
	for l in expr.splitlines():
		l = l.strip()
		if len(l) == 0: continue
		if l[0] == '*': continue	# Skip comments
		l = l.replace("+", " + ")
		l = l.replace("-", " - ")
		l = l.replace("#", " # ")
		l = l.replace(":", " : ")
		l = l.replace("(", " ( ")
		l = l.replace(")", " ) ")
		lst.extend(l.split())
	return lst

# ----------------------------------------------------------------------
def splitZones(expr):
	"""split a tokenized expression into zones"""
	zones = []
	zone  = []
	depth = 0
	for token in expr:
		if token==":" and depth==0:
			if zone:
				zones.append(zone)
				zone = []
			continue

		elif token == "(":
			depth += 1

		elif token == ")":
			depth -= 1
			if depth<0:
				raise CSGException("Too many closing parenthesis")

		zone.append(token)

	if zone: zones.append(zone)
	return zones

# ----------------------------------------------------------------------
def toString(expr):
	"""return a string version of a tokenize expression"""
	s    = ""
	prev = "("
	for token in expr:
		if prev == "(":
			s += token
		elif token == ":":
			s += " : "
		elif token in ("+", "-"):
			s += " %s"%(token)
		else:
			s += token
		prev = token
	return s

# ----------------------------------------------------------------------
def check(expr):
	"""check depth of an rpn expression"""
	depth = 0
	for token in expr:
		if token in ("+", "-", ":"):
			depth -= 1
		else:
			depth += 1
	return depth == 1

# ----------------------------------------------------------------------
# Subroutine:	exp2rpn
# Author:	Vasilis.Vlachoudis@cern.ch
# Date:		20/4/2004
#
# Convert the FLUKA Boolean expression to Reverse Polish Notation (RPN)
# Since the normalization routine does not accept the +/- as signs to
# objects, the routine is converting the leading - to @- (Universe minus)
# where the special symbol @ is treated as the universe.
# Furthermore the leading + is ignored as well as the leading | which is
# accepted by fluka.
#
# WARNING: No check is done for the correctness of the expression apart
#          from the parenthesis nesting
#
# ie.
#        A+B         -> A B +
#       (A+B)|C      -> A B + C |
#       (A|B)|C+D|E  -> A B | C D + | E |
#       -A           -> @ A -
#       -(-A)        -> @ @ A - -
#
# The routine is using the same array for returning the Reverse Polish
# expression, since the format is more compact.
# This is generally true apart one case -A -> @ A -
#
# Priorities are treated as:
#     Operator  Priority         In     Out
#     --------  --------        ---     ---
#       |       lower             1       2
#       +       high              3       4
#       -       high              3       4
#       (       higher           99       0
#       )       higher            0      99
#       object  highest         101     100
#
# Algorithm
#  Consider the expression as a train moving on a railroad with a
#  T-shape, where each token is one wagon
#
#                      <-  (A|B)|C+D
#      ------------.   .------------
#      RPN-End      \ /      Exp-End
#                    |
#                   S|
#                   t|
#                   a|
#                   c|
#                   k|
#
#  Each wagon to move from the Exp-End to the RPN-End it has to make
#  a stop first in the Stack-End. Before entering in the stack, the
#  priority-IN will be checked against the objects in the stack.
#  All top-most objects currently present in the stack with
#  higher priority-OUT will be transfered from the stack to the
#  RPN-End. Apart from the opening parenthesis ( which is discarded.
#
#  Example:
#  (1)                         A+B|C (1)
#  (2) A                        +B|C (2)
#  (3) A                         B|C (3)
#  (4) A                          |C (4)
#  (5) A B +                       C (5)
#  (6) A B + C
#  (7) A B + C |
#      ------------.   .------------
#      RPN-End      \ /      Exp-End
#                    |
#                   S|
#                   t|
#                   a|
#                   c|     B   C
#                   k| A + + | | |
#                      1 2 3 4 5 6 7
# ----------------------------------------------------------------------
def exp2rpn(expr):
	"""Replace expression list expr to rpn format"""
	#              Operator In Out
	priorities = {	"(" : [ 99,  0],
			":" : [  1,  2],
			"+" : [  3,  4],
			"-" : [  3,  4],
			")" : [  0, 99],
			" " : [101,100]}
	stack = []
	newproduct = 1
	i = 0
	m = 0
	while i<len(expr):
		tcur = expr[i]
		# Check for special leading chars
		if newproduct and (tcur==':' or tcur=='+'):
			newproduct = (tcur==':')
			i += 1
			continue

		if newproduct and tcur=='-':
			expr.insert(i,'*')	# insert space in ith position
			tcur = '@'      # Universe

		newproduct = (tcur=='(' or tcur==':')

		# Find priorities
		try:
			prio = priorities[tcur]
		except KeyError:
			prio = priorities[" "]

		ip = prio[0]
		op = prio[1]

		# Remove from the stack everything with higher priority
		while len(stack)>0 and ip<stack[-1][1]:
			if stack[-1][0] != '(':
				expr[m] = stack.pop()[0]
				m = m+1
			else:
				stack.pop()

		# Push it into the stack
		if tcur!=')':
			stack.append([tcur, op])
		else:
			# Should be an opening parenthesis
			if len(stack)==0:
				raise CSGException("Unbalanced parenthesis")
			stack.pop()

		#say("RPN=",expr[0:m])
		#say("STK=",stack)
		#print

		i += 1

	# Empty Stack
	while len(stack)>0:
		if stack[-1][0]=='(':
			raise CSGException("Unbalanced parenthesis")

		if m>=len(expr): expr.append("")
		expr[m] = stack.pop()[0]
		m = m+1

	# Delete unwanted items
	for i in range(len(expr)-1,m-1,-1):
		del expr[i]

# ----------------------------------------------------------------------
# Subroutine:	rpnorm
# Author:	Vasilis.Vlachoudis@cern.ch
# Date:		20/4/2004
#
# Normalize a CG expression given in Reverse Polish Notation.
# Normalized CG expression is an expression given as sum (Boolean OR) of
# products (Boolean intersection or subtraction).
# The normalization (expansion of parenthesis and operator priorities)
# should be performed by recursively calling the RPNRULE subroutine.
# Since Fortran-77 doesn't have recursion, call the RPNRULE for every
# operator starting from the right-most one, until no rule is found.
# ----------------------------------------------------------------------
def rpnorm(expr):
	# Loop until there is no any extra change needed

	# Scan to find the first operators
	changed = 1
	while changed:
		changed = 0
		i = len(expr)-1
		while i>=4:
			tx = expr[i]
			if tx in ('+', '-', ':'):
				l = len(expr)
				rule = _rpnrule(expr,i)
				if rule>0:
					changed = 1
					i += len(expr)-l+1
			i -= 1
			if len(expr) > MAXEXPR:
				raise CSGException("Expansion failed. Too many terms")

# ----------------------------------------------------------------------
# Subroutine:	_subTerms
# Author:	Vasilis.Vlachoudis@cern.ch
# Date:		20/4/2004
#
# This routine returns the pointers in the RPN terms array of the
# starting point of the left sub-expression LOWLEFT and right
# sub-expression LOWRIGHT given the pointer of the expr-operator NTX.
# The searching is performed by scanning from right to left the number
# of operators and objects pushed into the stack
#
# EXP          (expr-left) op (expr-right)
#
# RPN ...... | expr-left | expr-right | op | .......
#           Lowleft      LowRight  op-1 ntx
# ----------------------------------------------------------------------
def _subTerms(expr,n):

	nop = 0
	lowRight = 0
	lowLeft  = 0

	while n>=0:
		t = expr[n]
		if t=='+' or t=='-' or t==':':
			nop += 1
		else:
			nop -= 1

		n = n-1
		if nop==0:
			if lowRight==0:
				lowRight = n+1
				nop      = nop+1
				continue
			else:
				lowLeft = n+1
				return lowLeft,lowRight
	return lowLeft,lowRight

# ----------------------------------------------------------------------
# Subroutine:	rpnrule
# Author:	Vasilis.Vlachoudis@cern.ch
# Date:		20/4/2004
#
# Find a matching rule and apply it on the sub-expression starting from
# the N position in the Reverse Polish Notation
#
# An expression is in normal form when all the parenthesis are expanded
# and the expression is described as a sum (UNIONS) of products
# (INTERSECTIONS and/or SUBTRACTIONS)
#
# An expression can be converted to normal form by repeatedly applying
# the following set of production rules to the expression and then to its
# sub-expressions:
#
#    Normal Form                        Reverse Polish Notation
#  1. X-(Y|Z) -> (X-Y)-Z                X Y Z | -  ->  X Y - Z -
#  2. X+(Y|Z) -> (X+Y)|(X+Z)            X Y Z | +  ->  X Y + X Z + |
#  3. X-(Y+Z) -> (X-Y)|(X-Z)            X Y Z + -  ->  X Y - X Z - |
#  4. X+(Y+Z) -> (X+Y)+Z                X Y Z + +  ->  X Y + Z +
#  5. X-(Y-Z) -> (X-Y)|(X+Z)            X Y Z - -  ->  X Y - X Z + |
#  6. X+(Y-Z) -> (X+Y)-Z                X Y Z - +  ->  X Y + Z -
#  7. X|(Y|Z) -> (X|Y)|Z                X Y Z | |  ->  X Y | Z |
#  8. (X-Y)+Z -> (X+Z)-Y                X Y - Z +  ->  X Z + Y -
#  9. (X|Y)-Z -> (X-Z)|(Y-Z)            X Y | Z -  ->  X Z - Y Z - |
# 10. (X|Y)+Z -> (X+Z)|(Y+Z)            X Y | Z +  ->  X Z + Y Z + |
# X,Y, and Z here match both primitives or sub-expressions.
# ----------------------------------------------------------------------
def _rpnrule(expr,n):
	# Reset rule
	rule = 0

	# Top-most operator
	op  = expr[n]
	if op!='+' and op!='-' and op!=':': return rule

	# Right operator
	rop = expr[n-1]

	# Find left and right sub-trees
	ll,lr = _subTerms(expr,n)

	# Left operator
	lop = ' '
	if lr>0: lop = expr[lr-1]

	# Find Rule
	if   op=="-" and rop==":":
		rule = 1
	elif op=="+" and rop==":":
		rule = 2
	elif op=="-" and rop=="+":
		rule = 3
	elif op=="+" and rop=="+":
		rule = 4
	elif op=="-" and rop=="-":
		rule = 5
	elif op=="+" and rop=="-":
		rule = 6
	elif op==":" and rop==":":
		rule = 7
	elif op=="+" and lop=="-":
		rule = 8
	elif op=="-" and lop==":":
		rule = 9
	elif op=="+" and lop==":":
		rule = 10
	else:
		return rule

	# Find sub expressions X Y Z
	if rule<=7:    # X op (Y rop Z)
		Xu = lr-1
		Xl = ll

		ll,lr = _subTerms(expr,n-1)
		Yu = lr-1
		Yl = ll
		Zu = n-2
		Zl = lr
	else:		    # (X lop Y) op Z
		Zu = n-1
		Zl = lr
		L  = lr-1
		ll,lr = _subTerms(expr,L)
		Xu = lr-1
		Xl = ll
		Yu = L-1
		Yl = lr

	#say("Rule: ",rule)
	#say("X[",Xl,Xu,"]=",expr[Xl:Xu+1])
	#say("Y[",Yl,Yu,"]=",expr[Yl:Yu+1])
	#say("Z[",Zl,Zu,"]=",expr[Zl:Zu+1])
	#print

	# Expand the rule

	# 1. X-(Y|Z) -> (X-Y)-Z	 X Y Z | -  ->  X Y - Z -
	if    rule==1:
		# Leave X Y
		# Insert a - operator after Y
		expr.insert(Zl,"-")
		# Chop length by 1
		del expr[Zu+2]
		# Change the last operator to -
		expr[Zu+2] = '-'

	# 2. X+(Y|Z) -> (X+Y)|(X+Z)     X Y Z + |  ->  X Y + X Z + |
	elif rule==2:
		# Leave X Y
		# Insert a + operator after Y
		expr.insert(Zl,"+")
		# Copy X after the + operator
		to = Zl+1
		expr[to:to] = expr[Xl:Xu+1]
		Zu += Xu-Xl+2
		# Change last 2 operators to + |
		expr[Zu+1] = '+'
		expr[Zu+2] = '|'

	# 3. X-(Y+Z) -> (X-Y)|(X-Z)     X Y Z + -  ->  X Y - X Z - |
	elif rule==3:
		# Leave X Y
		# Insert a - operator after Y
		expr.insert(Zl,"-")
		# Copy X after the - operator
		to = Zl+1
		expr[to:to] = expr[Xl:Xu+1]
		Zu += Xu-Xl+2
		# Change last 2 operators to - |
		expr[Zu+1] = '-'
		expr[Zu+2] = '|'

	# 4. X+(Y+Z) -> (X+Y)+Z	 X Y Z + +  ->  X Y + Z +
	elif rule==4:
		# Leave X Y
		# Insert a + operator after Y
		expr.insert(Zl,"+")
		# Chop length by 1
		del expr[Zu+2]
		# Change the last operator to +
		expr[Zu+2] = '+'

	# 5. X-(Y-Z) -> (X-Y)|(X+Z)     X Y Z - -  ->  X Y - X Z + |
	elif rule==5:
		# Leave X Y
		# Insert a - operator after Y
		expr.insert(Zl,"-")
		# Copy X after the - operator
		to = Zl+1
		expr[to:to] = expr[Xl:Xu+1]
		Zu += Xu-Xl+2
		# Change last 2 operators to + |
		expr[Zu+1] = '+'
		expr[Zu+2] = '|'

	# 6. X+(Y-Z) -> (X+Y)-Z	 X Y Z - +  ->  X Y + Z -
	elif rule==6:
		# Leave X Y
		# Insert a + operator after Y
		expr.insert(Zl,"+")
		# Chop length by 1
		del expr[Zu+2]
		# Change the last operator to -
		expr[Zu+2] = '-'

	# 7. X|(Y|Z) -> (X|Y)|Z	 X Y Z | |  ->  X Y | Z |
	elif rule==7:
		# Leave X Y
		# Insert a | operator after Y
		expr.insert(Zl,":")
		# Chop length by 1
		del expr[Zu+2]
		# Change the last operator to |
		expr[Zu+2] = ':'

	# 8. (X-Y)+Z -> (X+Z)-Y	 X Y - Z +  ->  X Z + Y -
	elif rule==8:
		# Leave X
		# Copy "Z +" after X
		L = Zu-Zl+2
		to = Xu+1
		expr[to:to] = expr[Zl:Zl+L]
		# Delete old "Z +"
		del expr[Zl+L:Zl+L+L]

	# 9. (X|Y)-Z -> (X-Z)|(Y-Z)     X Y | Z -  ->  X Z - Y Z - |
	#10. (X|Y)+Z -> (X+Z)|(Y+Z)     X Y | Z +  ->  X Z + Y Z + |
	elif rule==9 or rule==10:
		# Leave X
		# Copy "Z -" or "Z +" after X
		L = Zu-Zl+2
		to = Xu+1
		expr[to:to] = expr[Zl:Zu+2]
		# Correct Z position
		Zl += L
		Zu += L
		# Delete the | infront of Z
		del expr[Zl-1]
		# Add | at the end
		expr.insert(Zu+1,":")

	return rule

# ----------------------------------------------------------------------
# Subroutine:	rpn2exp
# Author:	Vasilis.Vlachoudis@cern.ch
# Date:		20/4/2004
#
# Convert a NORMALIZED Reverse Polish notation to a standard expression
# WARNING: The routine expects an expression where for each UNION
# operator the right-sub-expression is a product while the left can be
# UNION or a product
# ----------------------------------------------------------------------
def rpn2exp(rpn):
	zones = []
	plus  = []
	minus = []

	i=0
	nstack = 0
	endprod = 0
	#say("RPN=",rpn)
	#say("LEN=",len(rpn))
	while i<len(rpn):
		tx = rpn[i]
		if tx=='+' or tx=='-' or tx==':':
			nstack -= 1
		else:
			# First term is always a plus
			# .. peek then next operator to check for sign
			if len(plus)==0 or rpn[i+1]=='+':
				plus.append(tx)
				lastPlus = 1
			elif rpn[i+1]=='-':
				minus.append(tx)
				lastPlus = 0
			nstack += 1

		if nstack==0:
			endprod = 1
		elif nstack==3:
			if lastPlus:
				del plus[-1]
			else:
				del minus[-1]
			i -= 2
			endprod = 1
		elif tx==':':
			i -= 2
			endprod = 1
		elif i==len(rpn)-1:
			#say(*,"END i=ntx")
			endprod = 1

		if endprod:
			optZone(plus,minus)
			# remove None terms
			plus  = filter(lambda x:x, plus)
			minus = filter(lambda x:x, minus)
			if len(plus)>0 or len(minus)>0:
				zones.append((plus,minus))
			plus    = []
			minus   = []
			nstack  = 0
			endprod = 0
		i += 1


	# Remove duplicates of products
	rmDoubles(zones)

	# Reconstruct expression
	expr = []
	for plus,minus in zones:
		if len(expr)>0 and expr[-1]!=":": expr.append(":")
		# Fill the new array
		for j in plus:
			expr.append("+")
			expr.append(j)
		for j in minus:
			expr.append("-")
			expr.append(j)

	return expr

# ----------------------------------------------------------------------
# Subroutine:	optZone
# Author:	Vasilis.Vlachoudis@cern.ch
# Date:		20/4/2004
#
# Optimize a product, by removing the universe @, duplicated terms like
# A+A, A-A, -A-A, and finally calling the geometrical optimizations and
# sorting by name the primitives in both the plus and minus terms.
#
# The product is described by 2 arrays the PLUS,NPLUS and MINUS,NMINUS
# with all the plus and minus terms of the product
#
# WARNING: It doesn't delete the term from the arrays but changes the
# name to space.
# ----------------------------------------------------------------------
def optZone(plus,minus):
	# Remove Universe @ from PLUS
	# and
	# remove duplicate terms A+A=A, A-A={}
	for i in range(len(plus)):
		if plus[i]=='@': plus[i]=None

		if plus[i]!=None:
			for j in range(i+1,len(plus)):
				if plus[i]==plus[j]: plus[j]=None
			for j in range(len(minus)):
				if plus[i]==minus[j]:
					# Remove everything
					del plus[:]
					del minus[:]
					return

	# Discard product if universe @ exists in MINUS
	# Check for duplicates in MINUS like -A-A=-A
	for i in range(len(minus)):
		if minus[i]=='@':
			# Remove everything
			del plus[:]
			del minus[:]
			return
		if minus[i]!=None:
			for j in range(i+1,len(minus)):
				if minus[i]==minus[j]: minus[j]=None

	# Perform the Geometrical optimization in the product
	#call OptGeo(nplus,plus,nminus,minus)

	# Peform a bubble sort on product terms
	plus.sort()
	minus.sort()

# ----------------------------------------------------------------------
# Subroutine:	rmDoubles
# Author:	Vasilis.Vlachoudis@cern.ch
# Date:		20/4/2004
#
# Remove duplicates of products A+B|A+B|C+D  ->  A+B|C+D
# ----------------------------------------------------------------------
def rmDoubles(zones):
	i = -1
	while i<len(zones)-1:
		i += 1
		plus1, minus1 = zones[i]
		j = i
		while j<len(zones)-1:
			j += 1
			plus2, minus2 = zones[j]

			# Check if they are the same
			if len(plus1)!=len(plus2) or len(minus1)!=len(minus2): continue
			diffplus = -1
			for k in range(len(plus1)):
				if plus1[k] != plus2[k]:
					diffplus = k
					break
			#if not same: continue

			diffminus = -1
			for k in range(len(minus1)):
				if minus1[k] != minus2[k]:
					diffminus = k
					break
			#if not same: continue

			if diffplus==-1 and diffminus==-1:
				del zones[j]
				j -= 1
				continue

# ----------------------------------------------------------------------
# Subroutine:	split
# Author:	Vasilis.Vlachoudis@cern.ch
# Date:		18/5/2004
#
# Break products into lists
# ----------------------------------------------------------------------
def split(expr):
	brk=[]
	expr=expr[:]	# Make a copy of the expression
	while 1:
		try:
			p = expr.index(":")
			brk.append(expr[0:p])
			del expr[0:p+1]
		except:
			brk.append(expr)
			return brk

# ----------
if __name__=="__main__":
	import sys, string, pprint
	from log import say

	expr = tokenize(string.join(sys.argv[1:]))

	say("Zones=")
	pprint.pprint(splitZones(expr))

	say("ZoneString=")
	pprint.pprint(map(toString, splitZones(expr)))

	say("ORG=",expr)

	exp2rpn(expr)
	say("RPN=",expr)

	rpnorm(expr)
	say("RPNORM=",expr)

	expnorm = rpn2exp(expr)
	say("NORM=",expnorm)

#	list = breakprod(expnorm)
	expr = string.join(expnorm)
	expr = expr.replace("+ ","+")
	expr = expr.replace("- ","-")
	say("EXP=",expr)
