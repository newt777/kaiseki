#!/usr/bin/env python
#input_data

class ListData:
    def __init__(self):
        self.strain = 0.0
        self.stress = 0.0
        self.wrapping = 0
    

#read
def read(file_name):
    file_object = open(file_name)
    lines = file_object.readlines()
    file_object.close
    data = [ListData()]
    
    #converting_to_list
    index = 0 
    for line in lines:
        items = line.split()
        data.append(ListData())
        data[index].strain = float(items[0])
        data[index].stress = float(items[1])
        index += 1
    return data

#wrapping_record
def nomal_wrapping(data):
    index = 1
    lenth = len(data)
    wrap_count = 0
    for index in range(lenth-1):
        if data[index].strain == 0:
             continue
        if (data[index].strain-data[index-1].strain) * (data[index].strain-data[index+1].strain) > 0: 
            wrap_count += 1
            #print data[index].strain,wrap_count
        data[index].wrapping = wrap_count
    return data

#noise_removal
def smooth_wrapping(data,target):
    target_index = 0
    wraplist_index = 0
    lenth_target = len(target)
    wraplist = [ListData()]
    
    for target_index in range(lenth_target-1):
        if target[target_index+1].wrapping > target[target_index].wrapping:
            wraplist.append(ListData())
            wraplist[wraplist_index] = target[target_index+1]
            wraplist_index += 1

    #data_smoothing & wrapping
    data_index = 1
    lenth_data = len(data)
    wraplist_index = 0
    start_data_index = 1 
    lenth_wraplist = len(wraplist)
    eps = 0.05
    del_index = 1
    del_count = 0
    smoothed_list = data
    wrap_count = 0
    for wraplist_index in range(lenth_wraplist-1):
        for data_index in range(start_data_index,lenth_data-3):
            start_data_index = data_index+1
            if (data[data_index].strain-data[data_index-1].strain) * (data[data_index].strain-data[data_index+1].strain) > 0:
                if abs(wraplist[wraplist_index].strain - data[data_index].strain) > eps:
                #    print wraplist[wraplist_index].strain,data[data_index+1].strain
                    del_index = data_index - del_count
                   # print "d"
                   # print data_index
                   # print del_index
                   # print wraplist_index
                   # print data[data_index].strain
                   # print wraplist[wraplist_index].strain
                    del smoothed_list[del_index]
                    del_count += 1
                    continue
                else:
                   # print "g"
                   # print data_index
                   # print del_index
                   # print data[data_index].strain
                   # print wraplist[wraplist_index].strain
                   # print wraplist_index
                    wrap_count += 1
                    smoothed_list[data_index-del_count].wrapping = wrap_count
                    break
            if abs(wraplist[wraplist_index].strain - data[data_index].strain) < eps and\
               data[data_index].strain == data[data_index+1].strain:
              # print "g"
              # print data_index
              # print del_index
              # print data[data_index].strain
              # print wraplist[wraplist_index].strain
              # print wraplist_index
               wrap_count += 1
               smoothed_list[data_index-del_count].wrapping = wrap_count
               break
            smoothed_list[data_index-del_count].wrapping = wrap_count
    return smoothed_list



#calculation
def residual_squre(firsts,seconds):
    first_index = 0
    second_index = 0
    second_start_index = 0
    lenth_firsts = len(firsts)
    lenth_seconds = len(seconds)
    total = 0
    for first_index in range(lenth_firsts-1):
        if second_start_index == lenth_seconds-2:     #end_decision
            break
        for second_index in range(second_start_index,lenth_seconds-1):
            if seconds[second_index].strain == firsts[first_index].strain:
                residual = firsts[first_index].stress - seconds[second_index].stress
                total += residual ** 2
                second_start_index = second_index
                print firsts[first_index].strain,firsts[first_index].stress,firsts[first_index].wrapping,first_index
                #print seconds[second_index].strain,seconds[second_index].stress,seconds[second_index].wrapping
                break
            if (firsts[first_index].strain - seconds[second_index].strain) * (firsts[first_index].strain - seconds[second_index+1].strain) < 0:
                residual =  ((firsts[first_index].strain - seconds[second_index].strain) * (seconds[second_index+1].stress - seconds[second_index].stress)\
                            / (seconds[second_index+1].strain - seconds[second_index].strain) + seconds[second_index].stress) - firsts[first_index].stress
                if firsts[first_index].wrapping != seconds[second_index].wrapping:
                   # import pdb;pdb.set_trace()
                    continue                    
                total += residual ** 2
                second_start_index = second_index
                print firsts[first_index].strain,firsts[first_index].stress,firsts[first_index].wrapping,first_index
                #print seconds[second_index].strain,seconds[second_index].stress,seconds[second_index].wrapping
                break
    return total

#def answer():
#    reply =''
#    while (reply == 'n' or 'y'):
#        input reply('do you want this here?')
#        if not reply =='n' or 'y':
#            print "please hit y or n!"
#    if reply == 'n':
#    elif reply == 'y':
#        input()
#    else:

