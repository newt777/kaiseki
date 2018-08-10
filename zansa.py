#!/usr/bin/env python
import sys
import zansa_calc
import csv
"---------------------------------------------------------------------------------------------------------------------------------------------------"
"""script"""
args = sys.argv

"""
read localfile
"""
ExData = zansa_calc.read(args[1])
NmData = zansa_calc.read(args[2])

"""
wrapping_record
"""
ExData = zansa_calc.nomal_wrapping(ExData)

"""
noise_removal & wrapping_record
"""
NmData = zansa_calc.smooth_wrapping(NmData,ExData)

"""
calculation
"""
result = zansa_calc.residual_squre(ExData,NmData)


#"""
#record_stock
#"""
#f = open('output.csv', 'w')
#writer = csv.writer(f, lineterminator='\n')
#csvlist  []
#csvlist.append("hoge")
#csvlist.append("fuga")
#write.writerow(csvlist)

#reply = input("do you want this here? y/n")
#answer(reply)

print 'residual_squre = ' + str(result)

