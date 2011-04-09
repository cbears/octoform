scaledFilter = \
[ [ -20, -20, -20, -18, -16, -14, -12, -10,  -8,  -6,   0,   0,   0,   0,   0,   0,   0,   0, -50, -50, -50, -50, -50, -50 ],
  [ -25,  -5,  -2,  -1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 0, 0, -50, -50, -50, -50 ],
  [ -25,  -5,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 0, 0, -50, -50, -50, -50 ],
  [ -25,  -5,   5,   5,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2, 0, 0, -50, -50, -50, -50 ],
  [ -25,  -5,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1, 0, 0, -50, -50, -50, -50 ],
  [ -25,  -5,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 0, 0, -50, -50, -50, -50 ],
  [ -20, -20, -20, -18, -16, -14,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  -2,  -2, -25, -50 -50, -50, -50, -50, -50 ],
  [  -5,  -5,  -5,  -5,  -5,  -5,  -5,  -5,  -5,  -5,  -5,  -5,  -5,  -5,  -5,  -5,  -5,  -5, -50, -50 -50, -50, -50, -50, -50 ],
]

leftEdgeFilterSmall=\
[ [ -10, -10, -10, -10, -10,   0,   0, 0, 0, 0, -10],
  [  -8,  -6,   0, 3,   3,   3,   3,   3, 0, 0,  -10],
  [  -7,  -4,   0, 3,   3,   3,   3,   3, 0, 0,  -10],
  [  -6,  -2,   0, 3,   3,   3,   3,   3, 0, 0, -10],
]

rightEdgeFilterSmall = [ x[::-1] for x in leftEdgeFilterSmall ]

leftEdgeFilterSoft = \
[ [ -10, -10, -10, -10, -10, -10, -10, 0, 0, 0, -10],
  [  -8,  -6,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [  -7,  -4,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [  -6,  -2,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [  -5,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [  -4,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [  -3,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [  -2,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [  -1,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   0,   3,   3,   3,   3,   3, 0, 0, 0, -10],
  [   0,   1,   2,   3,   3,   3,   2, 1, 0, 0,  -4],
  [   0,   1,   2,   3,   3,   3,   2, 1, 0, 0,  -4],
  [   0,   1,   2,   3,   3,   3,   2, 1, 0, 0,  -4],
  [   0,   1,   2,   3,   3,   3,   2, 1, 0, 0,  -4],
  [   0,   1,   2,   3,   3,   3,   2, 1, 0, 0,  -4],
  [   0,   1,   2,   3,   3,   3,   2, 1, 0, 0,  -4],
  [   0,   1,   2,   3,   3,   3,   2, 1, 0, 0,  -4],
  [   0,   1,   2,   3,   3,   3,   2, 1, 0, 0,  -4],
  [   0,   2,   2,   3,   3,   3,   2, 2, 0, 0,  -4],
  [   0,   2,   2,   3,   3,   3,   2, 2, 0, 0,  -4],
  [   0,   2,   2,   3,   3,   3,   2, 2, 0, 0,  -4],
  [   0,   2,   2,   3,   3,   3,   2, 2, 0, 0,  -4],
  [   0,   2,   2,   3,   3,   3,   2, 2, 0, 0,  -4],
  [   0,   2,   2,   3,   3,   3,   2, 2, 0, 0,  -4],
  [   0,   2,   2,   3,   3,   3,   2, 2, 0, 0,  -4],
  [   0,   2,   2,   3,   3,   3,   2, 2, 0, 0,  -4],
  [   0,   2,   2,   3,   3,   3,   2, 2, 0, 0,  -4],
  [   0,   2,   2,   3,   3,   3,   2, 2, 0, 0,  -4],
]

rightEdgeFilterSoft = [ x[::-1] for x in leftEdgeFilterSoft ]

leftEdgeFilterHard = \
[ [ -20, -20, -20, -20, -20, -20, -20, 0, 0, 0],
  [ -16,   0,   0,   0,   0,   0,   0, 0, 0, 0],
  [ -12,   2,   3,   3,   3,   2,   0, 0, 0, 0],
  [ -10,   2,   3,   3,   3,   2,   0, 0, 0, 0],
  [  -8,   2,   3,   3,   3,   2,   0, 0, 0, 0],
  [  -6,   2,   3,   3,   3,   2,   0, 0, 0, 0],
  [  -5,   2,   3,   3,   3,   2,   0, 0, 0, 0],
  [  -4,   2,   3,   3,   3,   2,   0, 0, 0, 0],
  [  -4,   2,   3,   3,   3,   2,   0, 0, 0, 0],
  [  -4,   2,   3,   3,   3,   2,   0, 0, 0, 0],
  [  -4,   2,   3,   3,   3,   2,   0, 0, 0, 0],
  [  -4,   2,   3,   3,   3,   2,   0, 0, 0, 0],
]

rightEdgeFilterHard = [ x[::-1] for x in leftEdgeFilterHard ]

"""
print "*********************************************************************************"
for x in scaledFilter:
  y = [ "%04d" % i for i in x ]
  print " ".join(y)
print "*********************************************************************************"
for x in leftEdgeFilterSoft:
  print x
print "*********************************************************************************"
for x in rightEdgeFilterSoft:
  print x
print "*********************************************************************************"
for x in leftEdgeFilterHard:
  print x
print "*********************************************************************************"
for x in rightEdgeFilterHard:
  print x
print "*********************************************************************************"
"""
