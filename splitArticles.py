# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 21:57:29 2016

@author: Annie Tran
"""




n=1
with open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/Oakland2010/grantFull.txt') as textfile:
    content = textfile.read().splitlines()
    content=content[2:]
    file= open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/Oakland2010/grant{0}.txt'.format(n),'w')    
    for row in content:
        file.write(row)
        file.write('\n')
        if 'of 999 DOCUMENTS' in row:
            file.close()
            n=n+1
            file= open('/Users/isarasuntichotinun/Desktop/ANNIE/CSC 591/Data/Oakland2010/grant{0}.txt'.format(n),'w')
         
file.close()

            
            
  