#!/usr/bin/env python

## Author: somian (Soren Andersen) somian08 .at. gmail .doowaap. com
## benecurrit.py - validates env PATH, adds appropriate addtnl dirs
## Terms of ReUse: GPL v2 or later.
import os, sys, string, re
from stat import *

def pathelsFromEnv() :
    i_cnt = 0
    possP = { }
    allP  = [ ]
    # os.getenv('PATH') is another way
    for pathel in os.environ.get('PATH').split(os.pathsep) :
        possP[i_cnt] = pathel
        if os.path.exists(pathel) and os.path.isabs(pathel) and os.path.isdir(pathel) :
            if pathel != '/usr/games' and os.access(pathel, os.R_OK|os.X_OK) :
               if hasExeLF(pathel) : allP.append( pathel )

        i_cnt += 1
    return [ possP , tuple(allP) ]

def hasExeLF(pathel) :
    for pf in os.listdir(pathel) :
       fqpn = os.path.join(pathel,pf)
       flmd = os.stat(fqpn)[ST_MODE]
       if S_ISDIR(flmd): continue
       if S_IXUSR | flmd : return True


def main() :
      truePath = [ ]
      s = ""
      t = '''
The PATH variable for this process holds the pathels
'''
      b = '''
The filtered PATH will contain these pathel entries:
'''
      vB = pathelsFromEnv()
      pD = dict(vB[0])
      pV = vB[1]
      pK = pD.keys()
      pK.sort()
      for ps in pK :
          s += "        " + str(ps) + "  " + pD[ps] + "\n"

      sys.stderr.write(t + s + b)

      for item in heurForArchBins() :
          w122 = "  " + item
          sys.stderr.write( w122 + "\n" )
          truePath.append(item)

      for pvalid in pV :
          w222 = "  " + pvalid
          sys.stderr.write( w222 + "\n" )
          if not truePath.count(pvalid) : truePath.append(pvalid)

      sys.stderr.write( '''
The PATH shall henceforth be:
''' )
      print ':'.join(truePath)

def heurForArchBins() :
    ARCH_RE = re.compile('i[3456]86[-_]linux([-_]gnu)?')
    more_b_dir = [ ]

    def _chq(arg, dirname, names) :
      for elat in names :
         fqpn = os.path.join(dirname,elat)
         thisbin = os.path.join(fqpn, 'bin')
         if   (not os.path.isdir(fqpn)) \
          and (not os.path.islink(fqpn)) : del elat; continue
         if not re.search(arg,elat) :      del elat; continue
         sys.stderr.write("Detected " + fqpn + "\n")
         if os.path.exists(thisbin) and hasExeLF(thisbin) :
             uq = True
             for wob in more_b_dir :
               if os.path.samefile(thisbin, wob) : uq = False
             if uq :  more_b_dir.append(thisbin)

    for topd in '/usr/local', '/opt' :
        os.path.walk(topd, _chq, ARCH_RE)

    return more_b_dir


# Put the code from http://paste.pound-python.org/show/1958/
# here and set os.environ.set('PATH')
#  ...or os.putenv(varname, value)

# def execUnderNewEnv()


if __name__ == '__main__':
    main()

