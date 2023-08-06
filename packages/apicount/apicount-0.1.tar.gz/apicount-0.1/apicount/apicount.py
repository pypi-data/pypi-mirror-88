'''
apicount.py

Show list of APIs and count

Purpose
=======
    This program is used to list all apis in given directory or files 

    Usecases:
            - Compare API count and API signatures between two sources
            - API Counts to understand the fundamental complexity of program

Usage: usage : apicount.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -a, --showall         Show all apis with signatures
  -f FILENAME, --file=FILENAME
                        filename
  -d DESTNDIR, --destn=DESTNDIR
                        Destination Directory
  -t, --tree            Show All Directory Sources

'''
import re
import pdb
import collections
import os

CFileXtens = {
    #######
    # C/C++, Makefiles
    ##########
    "c"             :  { 'desc' : "C Source"},
    "h"             :  { 'desc' : "Header"},
    "cc"            :  { 'desc' : "Gnu C++ Source"},
    "cp"            :  { 'desc' : "Win C++ Source"},
    "cpp"           :  { 'desc' : "Win C++ Source"},
    "cxx"           :  { 'desc' : "Cxx C++ Source"},
    "include"       :  { 'desc' : "includes"},
    "inc"           :  { 'desc' : "inc Includes"},
}


CKeyWords = {
    #######
    # C/C++ Keywords
    #######
    "if"        : "conditional if",
    "else"      : "conditional else",
    "for"       : "for loop",
    "while"     : "while loop",
    "switch"    : "switch loop",
    "return"    : "return statements"
}

CLibKeyWords = {
    #######
    # C/C++ Lib Keywords
    #######
    "malloc"   : " ",
    "sizeof"   : " ",
    "memcmp"   : " ",
}

commentSymbol = "//"

"""
file -> {
        "count" : count,
        "funcs" :  {funcname, signature}
        "loc"   : {
                "line" : 
                "blank" :
                "comment" :
            }
         }
"""

"""
fpattern
   (\w+)        # Match on api
   (\([\w\n\r\t\s,<>\\\[\]\"\-.=&':/*]*\)[\s\t\n\r]*)
                # signature between ( )
   ([{]|[;]|.*?\*\/|.*?\/\/)   # ending with ';' or '}'
   (?:....) - match but don't group

    Match Comment lines:  (?:/\*(.*?)\*/)|(?://(.*?)\n)

"""
cpattern = r"(\w+)[\s\t\n\r]*(\([\w\n\r\t\s,<>|\\\[\]\"\-.=&':/*\(\)]*\)[\s\t\n\r]*)([{]|[;]|.*?\*\/|.*?\/\/)"
fpattern = r"(.*?)(\w+)[\s\t\n\r]*(\([\w\n\r\t\s,<>|\\\[\]\"\-.=&':/*\(\)]*\)[\s\t\n\r]*)([{]|.*?\*\/)"
npattern = r"[\s\t\n\r]*(\*|/\*|//)"

"""
subpattern
   (\w+)       # Match on api
   (\([\w\n\r\t\s,<>\\\[\]\"\-.=&':/*]*\)[\s\t\n\r]*)
                # signature between ( )
   ((?![*][/])|[,]|[{]|[;])  # ending with ';' or '}'
"""
subpattern = r"(\w+)[\s\t\n\r]*(\([\w\n\r\t\s,<>|\\\[\]\"\-.=&':/*\(\)]*\)[\s\t\n\r]*)($|(?![*][/])|[,]|[{]|[;])"

class funcnode:
    def __init__(self):
        self.apifuncs = collections.OrderedDict()
        self.dirtree = collections.OrderedDict()
        self.showall = False
        self.destndir = os.path.abspath(os.curdir)
        self.filename = ""
        self.showdirtree = False
        self.lineCount = 0
        self.totalCommentLineCount = 0
        self.parseCmdLineOptions()

    def __del__(self):
        pass

    def __call__(self, *args, **kwargs):
        #get all extn Nodes
        self.parseCmdLineOptions()

    def showapis(self):

        if self.filename:
            self.apiadd(self.filename)
        else:
            self.apiparse(self.destndir)

        if self.showdirtree is True:
            self.showtreedir()
            return

        #for funcname in self.funcnodes.keys():
        #    self.showfunc(funcname)

        #print(self.apifuncs)
        for fname in sorted(self.apifuncs.keys()):
            #print("="*80);
            #print("%-40s : %d functions" %(fname,self.apifuncs[fname]["count"]))
            #print("="*80);
            for fn in sorted(self.apifuncs[fname]["funcs"].keys()):
                if self.showall:
                    print("%s (%s)" %(fn, self.apifuncs[fname]["funcs"][fn]))
                else :
                    print(" %s " %(fn))

            print("="*80);
            print("%-50s : %10s %10s" %("        FILE", "#LOC", "#FUNC"))
            print("="*80);
            print("%-50s : %10d %10d" %("   "+fname,
                 self.apifuncs[fname]["loc"]["line"], self.apifuncs[fname]["count"]))
            print("="*80);

    def showtreedircount(self):
        if self.showdirtree is False:
            return
        print("="*80);

        print("\n%s > %s \n" %("="*4,os.getcwd()))
        print("="*80);
        print("%-50s : %10s %10s" %("        FILE", "#LOC", "#FUNC"))
        print("="*80);
        for direntry in self.dirtree.keys():
            spaces = direntry.count(os.sep)
            dirname = re.sub(r"\./","",os.path.basename(direntry))
            print("%s/" %(dirname))
            fdir  = self.dirtree[direntry]
            fcount = {}
            for fname in fdir:
                if fname in self.apifuncs.keys():
                    funcname = fname
                    fcount[fname] = self.apifuncs[fname]["count"]
                    #print(" ",' '*4,"%-60s : %d " %(funcname,self.apifuncs[fname]["count"]))

            scount = sorted(fcount.items(), key=lambda x: x[1], reverse=True)
            for count in scount:
                funcname = os.path.basename(re.sub(r"\./","",count[0]))
                print("%-50s : %10d %10d" %("   "+funcname,
                    self.apifuncs[count[0]]["loc"]["line"],count[1]))
        print("="*80);

    def showtreedir(self):
        if self.showdirtree is False:
            return

        self.showtreedircount()

        if not self.showall:
            quit()

        for direntry in self.dirtree.keys():
            spaces = direntry.count(os.sep)
            dirname = re.sub(r"\./","",os.path.basename(direntry))
            print("\n%s/" %(dirname))
            print("-"*80)
            fdir  = self.dirtree[direntry]
            for fname in fdir:
                for fname in sorted(self.apifuncs.keys()):
                    funcname = os.path.basename(re.sub(r"\./","",fname))
                    print("\n%-50s : LOC# %d  FUNC# %d" %(
                            funcname,self.apifuncs[fname]["loc"]["line"],
                            self.apifuncs[fname]["count"]))
                    print("."*60)
                    for fn in sorted(self.apifuncs[fname]["funcs"].keys()):
                        print(' '*4,"%s (%s)" %(fn, self.apifuncs[fname]["funcs"][fn]))

    def linecount(self, src):

        fileLineCount = 0
        fileBlankLineCount = 0
        fileCommentLineCount = 0
        with open(src) as f:
            for line in f:
                fileLineCount += 1

                lineWithoutWhitespace = line.strip()
                if not lineWithoutWhitespace:
                    fileBlankLineCount += 1
                elif lineWithoutWhitespace.startswith(commentSymbol):
                    self.totalCommentLineCount += 1
                    fileCommentLineCount += 1

            codelines = fileLineCount - (fileBlankLineCount + fileCommentLineCount)
            self.lineCount += codelines

            self.apifuncs[src]["loc"]={}
            self.apifuncs[src]["loc"]["line"]=codelines
            self.apifuncs[src]["loc"]["comment"]=fileCommentLineCount

    def apiparse(self, dirnode):
            for parent, dirs, files in os.walk(dirnode): 
                if (".git" not in parent and
                    ".ACME" not in parent and
                    parent not in self.dirtree.keys()):
                    #print(parent, dirs, files)
                    self.dirnode = parent
                    self.dirtree[parent] = list()
                for fname in files:
                    filename = os.path.join(parent, fname)
                    if os.path.isfile(filename):
                        index=[it.start() for it in re.finditer('[.]',filename)]
                        extn = filename[index[-1] + 1:]
                        if extn in CFileXtens.keys():
                            self.filenode = filename
                            self.dirtree[parent].append(filename)
                            self.apiadd(filename)
                  
    def apinode(self, fnstr):
        fn = fnstr[0].strip(' \t\n\r')
        signature = fnstr[1].strip(' \t\n\r')

        # Ignore functions within comments
        if (len(fnstr[2]) > 1): return
        callee = False
        if (fnstr[2].strip(' \t\n\r')  == ';'): callee = True

        fsubexpr = re.compile(subpattern, re.I)
        fsubstr = fsubexpr.findall(signature)
        for subfunc in fsubstr:
            self.apinode(subfunc)

    def apifunctions(self, fname, fnstr):
        fn = fnstr[0].strip(' \t\n\r')
        signature = re.sub(r"\s+"," ", fnstr[1])
        signature.strip(' \t\n\r')

        if (fname not in self.apifuncs.keys()):
            self.apifuncs[fname]={}
            self.apifuncs[fname]["funcs"]={}
            self.apifuncs[fname]["count"]=0

        if (fn not in self.apifuncs[fname]["funcs"].keys()):
            self.apifuncs[fname]["funcs"][fn]=signature
            self.apifuncs[fname]["count"] += 1
            #print(self.apifuncs[fname]["funcs"])
                
    def apiadd(self, src):
        #print(""*4,"-",src)

        with open(src) as fd:
            bufstr = fd.read()
            fexpr = re.compile(fpattern, re.I)
            nexpr = re.compile(npattern, re.I)
            fstr = fexpr.findall(bufstr)
            #print(fstr)
            
            for func in fstr:
                keywordfilter = re.findall(r"[\s\t\n\r]*(switch|for|if|while)[\!\(\s\t]*", func[0])
                startcomment = re.findall(r"[\s\t\n\r]*(\*|/\*|//)", func[0])
                endcomment = re.findall(r"(\*/|//)", func[3])
                #print("X%s,X%s,==> %s, %s" %(func[0], func[1],func[2],func[3]))
                #print(startcomment,keywordfilter, endcomment, ":", func[1:2])
                if not startcomment and not endcomment and not keywordfilter:
                    if (func[1] not in CKeyWords.keys() and func[1] not in CLibKeyWords.keys()):
                        #print(func)
                        if not func[1].isupper(): # Assuming macro is all upper case
                            self.apinode(func[1:])
                            self.apifunctions(src,func[1:])
                            self.linecount(src)

    def parseCmdLineOptions(self):
        level = 0

        from optparse import OptionParser
        usage = "apicount [options]"
        version = "%prog 1.0"
        parser = OptionParser(usage=usage, version=version)

        parser.add_option("-a", "--showall", action="store_true",
                            dest="showall", default=False,
                            help="Show all apis with signatures")
        parser.add_option("-f", "--file", action="store", type="string",
                            dest="filename", help="filename")
        parser.add_option("-d", "--destn", action="store", type="string",
                            dest="destndir",default=os.curdir,
                            help="Destination Directory")
        parser.add_option("-t", "--tree", action="store_true",
                            dest="showdirtree",default=False,
                            help="Show All Directory Sources")
        (options, args) = parser.parse_args()

        #print (options)

        if options.showall is True:
            self.showall = True

        if (options.destndir):
            self.destndir = options.destndir

        if (options.filename):
            self.filename = options.filename

        if (options.showdirtree is True):
            self.showdirtree = True

