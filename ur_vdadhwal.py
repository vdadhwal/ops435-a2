#!/usr/bin/env python3
#Student ID: vdadhwal

'''
OPS435 Assignment 2 - Winter 2020
Program: ur_vdadhwal.py
Author: "Vaishali Dadhwal"
The python code in this file ur_vdadhwal.py is original work written by
"Vaishali Dadhwal". No code in this file is copied from any other source 
including any person, textbook, or on-line resource except those provided
by the course instructor. I have not shared this python file with anyone
or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and violators 
will be reported and appropriate action will be taken.


   authorship declaration
   __author__ Vaishali Dadhwal
   __date__ 28 March 2020
   

'''

import os
import sys
import time
import argparse




def display_username(recs):
    namelist = set()
    for x in recs:
        namelist.add(x[0])
    return namelist

def display_host(recs):
    hostlist = set()
    for x in recs:
        hostlist.add(x[2])
    return hostlist


def read_login_rec(filelist):
    ''' docstring for this function
    get records from given filelist
    open and read each file from the filelist
    filter out the unwanted records
    add filtered record to list (login_recs)'''
   #usage_data_file:

    f=open(filelist,'r')

    recs=f.read().strip().split('\n')
    goodrecs = []
    for x in recs :
         rec=x.split()
         if len(rec) == 15:
            goodrecs.append(rec)
    return goodrecs


#time module:

   #fmt="%b %d %H:%M:
   #time.strptime(t_in, fmt) - time tuple

   #time.struct_time(tm_year=2018, tm_mon=2, tm_mday=13, tm_hour=16, tm_min=53, tm_sec=42, tm_wday=1, tm_yday=44, tm_isdst=-1)

   #time.strptime(t_out,fmt)

   #time.struct_time(tm_year=2018, tm_mon=2, tm_mday=13, tm_hour=16, tm_min=57, tm_sec=2, tm_wday=1, tm_yday=44, tm_isdst=-1)


  #in_tup = time.strptime(t_in,"%b %d %H:%M:%S %Y")
  #out_tup = time.strptime(t_out,"%b %d %H:%M:%S %Y")


  #diff_tup = float(time.strftime("%s",out_tup)) - float(time.strftime("%s",in_tup))


def normalized_rec(rec):
    '''Normalize login record produced by the last command.
       The login and logout time could be or not be on the same day.
       eg: (1) Mon Jan 01 12:23:34 2018 - Mon Jan 01 22:11:00 2018
       or  (2) Mon Jan 01 23:10:45 2018 - Tue Jan 02 00:15:43 2018
       or  (3) Mon Jan 01 09:00:23 2018 - Fri Jan 05 17:00:07 2018
       The login and logout time for (1) are on the same day, this
       record does not need to be normalized.
       The login and logout time for (2) are on two different days,
       after normalization, two records will be generated:
           (a) Mon Jan 01 23:10:45 2018 - Mon Jan 01 23:59:59 2018
           (b) Tue Jan 02 00:00:00 2018 - Tue Jan 02 00:15:43 2018
       The login and logout time for (2) spawn 5 days, after
       normalization, 5 records will be generated:
           (a) Mon Jan 01 09:00:23 2018 - Mon Jan 01 23:59:59 2018
           (b) Tue Jan 02 00:00:00 2018 - Tue Jan 02 23:59:59 2018
           (c) Wed Jan 03 00:00:00 2018 - Wed Jan 03 23:59:59 2018
           (d) Thu Jan 04 00:00:00 2018 - Thu Jan 04 23:59:59 2018
           (e) Fri Jan 05 00:00:00 2018 - Fri Jan 05 17:00:07 2018
                    4   5    6       7  8  9  10  11    12     13
          same day -> retrun the same record
          different days: 1st record -> keep login date/time
                                        change logout date
                                        (update fields 9,10,11,12)
                                        logout time-> 23:59:59
                          2nd record -> login day  +1 (update fields 3,4,5,7)
                                        time -> 00:00:00
                                        keep logout date/time
          pass the 2nd record to the normalized_rec function again
          Please note that this is a recursive function.
    '''
    jday = time.strftime('%j',time.strptime(' '.join(rec[4:6]+rec[7:8]),'%b %d %Y'))
    jday2 = time.strftime('%j',time.strptime(' '.join(rec[10:12]+rec[13:14]), '%b %d %Y'))
    if jday == jday2:
       norm_rec = []
       norm_rec.append(rec.copy())
       return norm_rec
    else:
       # calculate next day string in 'WoD Month Day HH:MM:SS YYYY'
       new_rec1 = rec.copy()
       new_rec = rec.copy()
       t_next = time.mktime(time.strptime(' '.join(new_rec1[4:6]+rec[7:8]),'%b %d %Y'))+86400
       next_day = time.strftime('%a %b %d %H:%M:%S %Y',time.strptime(time.ctime(t_next))).split()
       new_rec1[12] = '23:59:59'
       new_rec1[9] = new_rec1[3]
       new_rec1[10] = new_rec1[4]
       new_rec1[11] = new_rec1[5]
       new_rec[3] = next_day[0] # Day of week Sun, Mon, Tue...
       new_rec[4] = next_day[1] # Month Jan, Feb, Mar, ...
       new_rec[5] = next_day[2] # Day of Month 01, 02, ...
       new_rec[6] = next_day[3] # Time HH:MM:SS
       new_rec[7] = next_day[4] # Year YYYY
       norm_rec = normalized_rec(new_rec)
       normalized_recs = norm_rec.copy()
       normalized_recs.insert(0,new_rec1)  # call normalized_rec function recursive
    return normalized_recs

    return diff_tup

def cal_daily_usage(subject,login_recs):
    ''' docstring for this function
    generate daily usage report for the given
    subject (user or remote host)'''
    daily_usage = {}
    daily_records = []

    daily_line = "Daily Usage Report for ", str(args.rhost)
    in_take = args.rhost
    record = 2

    if args.user:
        daily_line = "Daily Usage Report for ", str(args.user)
        in_take = args.user
        record = 0

    for item in login_recs:
        if item[record] == in_take:
            daily_records.append(item)
    for item in daily_records:
        final_date = time.strftime('%Y %m %d',time.strptime(''.join(item[7]+item[4]+item[5]), '%Y%b%d'))

        start_time = time.strftime('%s',time.strptime(item[6],'%H:%M:%S'))

        end_time = time.strftime('%s',time.strptime(item[12], '%H:%M:%S'))

        time_diff = int(end_time) - int(start_time)

        if final_date in list(daily_usage.keys()):

        	daily_usage[final_date] += time_diff

        else:

        	daily_usage[final_date] = time_diff

    print(daily_line)
    print("=" * len(daily_line))
    print("Date      Usage in Seconds")

    for dates , day_time_secs in sorted(daily_usage.items(),reverse=True):
        print('%-13s %13s'% (dates, day_time_secs))
    total =0

    for item in daily_usage.values():

        total += item

    print('%-13s %13s'% ("Total", total))

def cal_weekly_usage(subject,login_recs):
    ''' docstring for this function
    generate weekly usage report for the given
    subject (user or remote host)'''

    weekly_usage = {}

    weekly_records = []


    weekly_line = "Weekly Usage Report for " + str(args.rhost)

    in_take = args.rhost

    record = 2


    if args.user:

    	weekly_line = "Weekly Usage Report for " + str(args.user)

    	in_take = args.user

    	record = 0


    for item in login_recs:

    	if item[record] == in_take:

    		weekly_records.append(item)


    for item in weekly_records:

    	final_date = time.strftime('%Y %W',time.strptime(''.join(item[7]+item[4]+item[5]), '%Y%b%d'))

    	start_time = time.strftime('%s',time.strptime(item[6],'%H:%M:%S'))

    	end_time = time.strftime('%s',time.strptime(item[12], '%H:%M:%S'))

    	time_diff = int(end_time) - int(start_time)

    	if final_date in list(weekly_usage.keys()):

    		weekly_usage[final_date] += time_diff

    	else:

    		weekly_usage[final_date] = time_diff


    print(weekly_line)

    print("=" * len(weekly_line))

    print("Week #       Usage in Seconds")


    for dates, week_time_secs in sorted(weekly_usage.items(), reverse=True):

    	print('%-13s %13s'% (dates, week_time_secs))


    total = 0

    for item in weekly_usage.values():

    	total += item

    print('%-13s %13s'% ("Total", total))


def cal_monthly_usage(subject,login_recs):
    ''' docstring for this function
    generate monthly usage report fro the given
    subject (user or remote host)'''


    monthly_usage = {}

    monthly_records = []


    monthly_line = "Monthly Usage Report for " + str(subject)

    if subject == args.rhost:

    	subject = args.rhost

    else:

    	subject = args.user

    record = 2
    if subject == args.user:
        monthly_string = "Monthly Usage Report for " + str(subject)
        record = 0

    for item in login_recs:
        if item[record] == subject:
            monthly_records.append(item)



    for item in monthly_records:


        final_date = time.strftime('%Y %m',time.strptime(''.join(item[7]+item[4]+item[5]), '%Y%b%d'))


        start_time = time.strftime('%s',time.strptime(item[6],'%H:%M:%S'))


        end_time = time.strftime('%s',time.strptime(item[12], '%H:%M:%S'))


        time_difference = int(end_time) - int(start_time)


        if final_date in list(monthly_usage.keys()):


        	monthly_usage[final_date] += time_difference


        else:


        	monthly_usage[final_date] = time_difference



    print(monthly_line)


    print("=" * len(monthly_line))


    print("Month         Usage in Seconds")



    for dates, month_time_secs in sorted(monthly_usage.items(), reverse=True):


    	print('%-13s %13s'% (str(dates), int(month_time_secs)))



    total = 0


    for item in monthly_usage.values():


    	total += item


    print('%-13s %13s'% ("Total", total))


if __name__ == '__main__':

    #[ code to retrieve command line argument using the argparse module [

    parser = argparse.ArgumentParser(description="Usage Report based on the last command",epilog="Copyright 2019 - Garima Uppal")
    parser.add_argument("-l", "--list", type=str, choices=['user','host'], help="generate user name or remote host IP from the given files")
    parser.add_argument("-r", "--rhost", help="usage report for the given remote host IP")
    parser.add_argument("-t","--type", type=str, choices=['daily','weekly','monthly'], help="type of report: daily, weekly, and monthly")
    parser.add_argument("-u", "--user", help="usage report for the given user name")
    parser.add_argument("-v","--verbose", action="store_true",help="turn on output verbosity")
    parser.add_argument("files",metavar='F', type=str, nargs='+',help="list of files to be processed")
    args=parser.parse_args()
    if args.verbose:
        print('Files to be processed:',args.files)
        print('Type of args for files',type(args.files))
    if args.user:
        print('usage report for user:',args.user)
    if args.rhost:
        print('usage report for remote host:',args.rhost)
    if args.type:
       print('usage report type:',args.type)
    '''[ based on the command line option,
      call the appropriate functions defined about
      to read the login records,
      to process the login records
      to generate and print
      the requested usage report ]'''
    recs = []
    for filename in args.files:
        recs.extend(read_login_rec(filename))

    norm_recs = []
    for rec in recs:
        norm_recs.extend(normalized_rec(rec))

    if args.list == 'user':
        #subject_input = args.user
        namelist = display_username(recs)
        for username in namelist:
            print(username)

    if args.list == 'host':
        #subject_input = args.rhost
        hostlist = display_host(recs)
        for hostip in hostlist:
            print(hostip)

    if args.user:
        subject_input = args.user
    else:
        subject_input = args.rhost
    if args.type == 'daily':
        cal_daily_usage(subject_input , norm_recs)
    elif args.type == 'weekly':
        cal_weekly_usage(subject_input , norm_recs)
    elif args.type == 'monthly':
        cal_monthly_usage(subject_input , norm_recs)