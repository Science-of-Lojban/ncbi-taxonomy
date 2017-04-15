#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
from sys import argv
from ete3 import Tree
from ete3 import NCBITaxa
ncbi = NCBITaxa()
ncbi.update_taxonomy_database()

descendants = ncbi.get_descendant_taxa(argv[1], collapse_subspecies=False) #2759 - eukarya
names = ncbi.translate_to_names(descendants)

def Back(linn):
    linn=re.sub(r"^la ", "", linn,flags=re.UNICODE)
    #linn = r"la " + linn
    #- final
    linn = re.sub(r"\bku'a la\b", "x", linn,flags=re.UNICODE)
    #linn = re.sub(r"\bx\b", "ku'a la", linn,flags=re.UNICODE)
    #- special words
    linn = re.sub(r"c$", "", linn,flags=re.UNICODE)
    linn = re.sub(r"c(?!\')\b", "", linn,flags=re.UNICODE)
    linn = re.sub(r"y$", "", linn,flags=re.UNICODE)
    linn = re.sub(r"y(?!\')\b", "", linn,flags=re.UNICODE)
    #linn = re.sub(r"([aeiou])$", "\g<1>c", linn,flags=re.UNICODE)
    #linn = re.sub(r"([aeiou]) ", "\g<1>c ", linn,flags=re.UNICODE)
    #linn = re.sub(r"c(?![\'])(\b|$)", "cyc", linn,flags=re.UNICODE)
    linn = re.sub(r"kau'", "q", linn,flags=re.UNICODE)
    #treat 'q'
    #- add consonant to the end
    linn = re.sub(r"nydj", "ndj", linn,flags=re.UNICODE)
    linn = re.sub(r"nydz", "ndz", linn,flags=re.UNICODE)
    linn = re.sub(r"nytc", "ntc", linn,flags=re.UNICODE)
    linn = re.sub(r"nyts", "nts", linn,flags=re.UNICODE)
    linn = re.sub(r"myz", "mz", linn,flags=re.UNICODE)
    # linn = re.sub(r"ndj", "nydj", linn,flags=re.UNICODE)
    # linn = re.sub(r"ndz", "nydz", linn,flags=re.UNICODE)
    # linn = re.sub(r"ntc", "nytc", linn,flags=re.UNICODE)
    # linn = re.sub(r"nts", "nyts", linn,flags=re.UNICODE)
    # linn = re.sub(r"mz", "myz", linn,flags=re.UNICODE)
    #- the substrings mz, nts, ntc, ndz, ndj are not allowed
    linn = re.sub(r"([ckq])y(?=[x])", "\g<1>", linn,flags=re.UNICODE)
    linn = re.sub(r"([x])y(?=[ckq])", "\g<1>", linn,flags=re.UNICODE)
    # linn = re.sub(r"([ck])([x])", "\g<1>y\g<2>", linn,flags=re.UNICODE)
    # linn = re.sub(r"([x])([ck])", "\g<1>y\g<2>", linn,flags=re.UNICODE)
    #- x can't be next to c or k
    linn = re.sub(r"([cjsz])y(?=[cjsz])", "\g<1>", linn,flags=re.UNICODE)
    # linn = re.sub(r"([cjsz])([cjsz])", "\g<1>y\g<2>", linn,flags=re.UNICODE)
    #- sibilants (cjsz) can't be next to each other
    linn = re.sub(ur"([ptkqfscbdgvzjlmnrx])y(?=[ptkqfscbdgvzjlmnrx])", "\g<1>", linn,flags=re.UNICODE)
    # linn = re.sub(r"([ptkfscbdgvzjlmnrx])\1", "\g<1>y\g<1>", linn,flags=re.UNICODE)
    #- no consonant can be followed by itself
    linn = re.sub(r"([ptkqfsc])y(?=[bdgvzj])", "\g<1>", linn,flags=re.UNICODE)
    linn = re.sub(r"([bdgvzj])y(?=[ptkqfsc])", "\g<1>", linn,flags=re.UNICODE)
    # linn = re.sub(r"\|", "", linn,flags=re.UNICODE)
    # linn = re.sub(r"([ptkfscbdgvzj])([ptkfscbdgvzj])", "\g<1>y\g<2>", linn,flags=re.UNICODE)
    # linn = re.sub(r"([bdgvzj])([bdgvzj])", "\g<1>|\g<2>", linn,flags=re.UNICODE)
    # linn = re.sub(r"([ptkfsc])([ptkfsc])", "\g<1>|\g<2>", linn,flags=re.UNICODE)
    #- voiced consonants can't be next to voiceless ones, and vice versa
    linn = re.sub(r"([aeiou])'y", "\g<1>y", linn,flags=re.UNICODE)
    linn = re.sub(r"(u)'(?=[aeiou])", "\g<1>", linn,flags=re.UNICODE)
    linn = re.sub(r"(o)'(?=[aeou])", "\g<1>", linn,flags=re.UNICODE)
    linn = re.sub(r"(i)'(?=[aeiou])", "\g<1>", linn,flags=re.UNICODE)
    linn = re.sub(r"(e)'(?=[aeou])", "\g<1>", linn,flags=re.UNICODE)
    linn = re.sub(r"(a)'(?=[aeou])", "\g<1>", linn,flags=re.UNICODE)
    # linn = re.sub(r"([aeiouy])y", "\g<1>'y", linn,flags=re.UNICODE)
    # linn = re.sub(r"(u)([aeiou])", "\g<1>'\g<2>", linn,flags=re.UNICODE)
    # linn = re.sub(r"(o)([aeou])", "\g<1>'\g<2>", linn,flags=re.UNICODE)
    # linn = re.sub(r"(i)([aeiou])", "\g<1>'\g<2>", linn,flags=re.UNICODE)
    # linn = re.sub(r"(e)([aeou])", "\g<1>'\g<2>", linn,flags=re.UNICODE)
    # linn = re.sub(r"(a)([aeo])", "\g<1>'\g<2>", linn,flags=re.UNICODE)
    #- add ' between vowels
    linn = re.sub(r"([aeiouy])w(?=[aeiouy])", u"\g<1>u", linn,flags=re.UNICODE)
    linn = re.sub(ur"([aeiouy])ɩ(?=[aeiouy])", u"\g<1>i", linn,flags=re.UNICODE)
    # linn = re.sub(r"([aeiouy])(u)([aeiouy])", u"\g<1>w\g<2>", linn,flags=re.UNICODE)
    # linn = re.sub(r"([aeiouy])(i)([aeiouy])", u"\g<1>ɩ\g<2>", linn,flags=re.UNICODE)
    #- detect glides, krulermonize them
    linn = re.sub(r"'y([^aeiouy])", "'\g<1>", linn,flags=re.UNICODE)
    # linn = re.sub(r"'([^aeiouy])", "'y\g<1>", linn,flags=re.UNICODE)
    #- h must both follow and be followed by a vowel, diphthong, or y
    linn = re.sub(r"y'", "h", linn,flags=re.UNICODE)
    linn = re.sub(r"hwu", "hywu", linn,flags=re.UNICODE)
    #back addition
    linn = re.sub(r"hwi", "hywi", linn,flags=re.UNICODE)
    #back addition
    linn = re.sub(r"ywu", "yuu", linn,flags=re.UNICODE)
    linn = re.sub(r"ywi", "yui", linn,flags=re.UNICODE)
    linn = re.sub(r"yuu", "w", linn,flags=re.UNICODE)
    linn = re.sub(r"yui", "y", linn,flags=re.UNICODE)
    # linn = re.sub(r"[hH]", "y'", linn,flags=re.UNICODE)
    # linn = re.sub(r"yuu", "ywu", linn,flags=re.UNICODE)
    # linn = re.sub(r"yui", "ywi", linn,flags=re.UNICODE)
    # linn = re.sub(r"w", "yuu", linn,flags=re.UNICODE)
    # linn = re.sub(r"y", "yui", linn,flags=re.UNICODE)
    linn = re.sub(r"'", "h", linn,flags=re.UNICODE)
    #fix ' to h
    linn = re.sub(r"^h", "H", linn,flags=re.UNICODE)
    #fix case of "h"
    return linn

def pretoLojban(linn):
    linn = re.sub(r"('\b|\b')", "", linn,flags=re.UNICODE)
    linn = re.sub(r"'$", "", linn,flags=re.UNICODE).lower()
    return linn

def toLojban(linn):
    linn = pretoLojban(linn)
    linn = re.sub(r"y", "yui", linn,flags=re.UNICODE)
    linn = re.sub(r"w", "yuu", linn,flags=re.UNICODE)
    linn = re.sub(r"yui", "ywi", linn,flags=re.UNICODE)
    linn = re.sub(r"yuu", "ywu", linn,flags=re.UNICODE)
    linn = re.sub(r"[hH]", "y'", linn,flags=re.UNICODE)
    #h must both follow and be followed by a vowel, diphthong, or y:
    linn = re.sub(r"'([^aeiouy])", "'y\g<1>", linn,flags=re.UNICODE)
    #detect glides, krulermonize them:
    linn = re.sub(r"([aeiouy])i(?=[aeiouy])", u"\g<1>ɩ", linn,flags=re.UNICODE)
    linn = re.sub(r"([aeiouy])u(?=[aeiouy])", u"\g<1>w", linn,flags=re.UNICODE)
    #add ' between vowels:
    linn = re.sub(r"(a)(?=[aeou])", "\g<1>'", linn,flags=re.UNICODE)
    linn = re.sub(r"(e)(?=[aeou])", "\g<1>'", linn,flags=re.UNICODE)
    linn = re.sub(r"(i)(?=[aeiou])", "\g<1>'", linn,flags=re.UNICODE)
    linn = re.sub(r"(o)(?=[aeou])", "\g<1>'", linn,flags=re.UNICODE)
    linn = re.sub(r"(u)(?=[aeiou])", "\g<1>'", linn,flags=re.UNICODE)
    linn = re.sub(r"([aeiouy])y", "\g<1>'y", linn,flags=re.UNICODE)
    #voiced consonants can't be next to voiceless ones, and vice versa:
    linn = re.sub(r"([ptkqfsc])(?=[ptkqfsc])", "\g<1>|", linn,flags=re.UNICODE)
    linn = re.sub(r"([bdgvzj])(?=[bdgvzj])", "\g<1>|", linn,flags=re.UNICODE)
    linn = re.sub(r"([ptkqfscbdgvzj])(?=[ptkqfscbdgvzj])", "\g<1>y", linn,flags=re.UNICODE)
    linn = re.sub(r"\|", "", linn,flags=re.UNICODE)
    #no consonant can be followed by itself:
    linn = re.sub(r"([ptkqfscbdgvzjlmnrx])\1", "\g<1>y\g<1>", linn,flags=re.UNICODE)
    #sibilants (cjsz) can't be next to each other:
    linn = re.sub(r"([cjsz])(?=[cjsz])", "\g<1>y", linn,flags=re.UNICODE)
    #x can't be next to c or k:
    linn = re.sub(r"([x])(?=[ckq])", "\g<1>y", linn,flags=re.UNICODE)
    linn = re.sub(r"([ckq])(?=[x])", "\g<1>y", linn,flags=re.UNICODE)

    #the substrings mz, nts, ntc, ndz, ndj are not allowed:
    linn = re.sub(r"mz", "myz", linn,flags=re.UNICODE)
    linn = re.sub(r"nts", "nyts", linn,flags=re.UNICODE)
    linn = re.sub(r"ntc", "nytc", linn,flags=re.UNICODE)
    linn = re.sub(r"ndz", "nydz", linn,flags=re.UNICODE)
    linn = re.sub(r"ndj", "nydj", linn,flags=re.UNICODE)
    #add consonant to the end
    linn = re.sub(r"c(?![\'])(\b|$)", "cyc", linn,flags=re.UNICODE)
    linn = re.sub(r"([aeiou]) ", "\g<1>c ", linn,flags=re.UNICODE)
    linn = re.sub(r"([aeiou])$", "\g<1>c", linn,flags=re.UNICODE)
    #treat 'q'
    linn = re.sub(r"q", "kau'", linn,flags=re.UNICODE)
    #special words:
    linn = re.sub(r"\bx\b", "ku'a la", linn,flags=re.UNICODE)
    #final:
    linn = r"la " + linn
    return linn


"""
#test single name
linn = u"Nematanthus wettsteinii"
jbo = toLojban(linn)
bck = Back(jbo)
t = pretoLojban(linn) == bck
fin = linn + "\t" + jbo + "\t" + (bck) + "\t" + str(t)
print(fin)
"""

with open('eu-res.txt','w') as text_file:
    print ("co'a")
    for line in descendants:
        com = ncbi.get_common_names([line])
        linn = ncbi.translate_to_names([line])[0]
        jbo = toLojban(linn)
        bck = Back(jbo)
        t = pretoLojban(linn).lower() == bck.lower()
        fin = str(line) + "\t"+(jbo) + '\t' + linn.encode('utf-8') + "\t" + (bck) + "\t" + str(t)
        text_file.write(fin.encode('utf-8')+'\n')

print("mu'o")
