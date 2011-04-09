"""
  (c) Charles Shiflett 2011
"""
import random
try: 
  import hashlib 
except ImportError:
  import sha as hashlib

sysrand = random.SystemRandom()

def hash( s ):
  try:
    h=hashlib.sha256(secretHash)
  except AttributeError:
    h=hashlib.sha(secretHash)
  h.update(s)
  return h.hexdigest()

def genString( digits, type = "ASCII"):

  if type == "ASCII":
    genTwo = 61
  elif type == "HEX":
    genTwo = 16
  elif type == "DIGIT":
    genTwo = 9
  else:
    raise ValueError("Type specified incorrectly")

  if digits < 1:
    raise ValueError("# Digits < 1")

  randString = []
  for j in xrange ( 0, digits):
    k = sysrand.randint ( 0, genTwo )
    if k < 10:
      k += 0x30
    elif k < 36:
      k += 0x41 - 10
    else:
      k += 0x61 - 36
    randString.append( chr( k ) )
  return "".join( randString )

secretHash=genString( 64 )
