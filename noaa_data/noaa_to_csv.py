import urllib2, os

"""
Row character spec:
------------------------------
Variable   Columns   Type
------------------------------
ID            1-11   Character
YEAR         12-15   Integer
MONTH        16-17   Integer
ELEMENT      18-21   Character
VALUE1       22-26   Integer
MFLAG1       27-27   Character
QFLAG1       28-28   Character
SFLAG1       29-29   Character
VALUE2       30-34   Integer
MFLAG2       35-35   Character
QFLAG2       36-36   Character
SFLAG2       37-37   Character
  .           .          .
  .           .          .
  .           .          .
VALUE31    262-266   Integer
MFLAG31    267-267   Character
QFLAG31    268-268   Character
SFLAG31    269-269   Character
------------------------------
"""

# download weather data
#with open("noaa_ftp_data.dly", "w") as ftpfile:
#  for line in answer.readlines():
#    ftpfile.write(line)


elements_we_want = ["TMIN", "TMAX", "PRCP", "SNOW", "WSF2"]
# min temp, max temp, avg temp, precip, snowfall, fastest 2min wind speed

# take in a clump of month rows and turn it into 31 day rows
# month data is a dictionary from [element type] -> [list of 31 values]
def process_month_data(year, month, month_data, output_file_name):
    with open(output_file_name, "w+") as my_out_file:
        for day_index in range(0,31):
            a_line = []
            padded_day = format(day_index + 1, "02")
            a_line.append(year + month + padded_day)
            for element in elements_we_want:
                a_line.append(str(int(month_data[element][day_index])))
            my_out_file.write((",".join(a_line)) + "\n")

def process_whole_file(first_month, first_year, the_file, output_file_name):
    # Don't append to the file you're writing out to -- remove it
    #if os.path.isfile(output_file_name):
    #    os.remove(output_file_name) 

    month_data = {}
    last_seen_month = first_month
    last_seen_year = first_year
    for a_line in the_file.readlines():
        my_id = a_line[0:11]
        my_year = a_line[11:15]
        my_month = a_line[15:17]
        my_elem = a_line[17:21]

        # only want recent data, so skip if not after 2000
        if(int(my_year) < int(first_year)):
            continue
        elif int(my_year) == int(first_year) and int(my_month) < int(first_month):
            continue

        # write out the data for the month we've been reading when we get to a new month
        # keep track of last_seen so that it makes sense
        if my_month != last_seen_month:
            process_month_data(last_seen_year, last_seen_month, month_data, output_file_name)
            last_seen_month = my_month
            last_seen_year = my_year
            month_data.clear()

        # each line is an element - but only deal with it if we want the element
        if my_elem in elements_we_want:
            day_values = []
            for day_index in range(0, 31):
                # math for pulling out values around the flags
                value_index = 21 + (day_index * 8) 
                day_values.append(a_line[value_index:value_index + 5])
            month_data[my_elem] = day_values

    # once here, we've got one last month left loaded, process it
    # TODO: fix control flow so this extra process is built into the above loop
    process_month_data(last_seen_year, last_seen_month, month_data, output_file_name)

if __name__ == "__main__":
    first_month = "01"
    first_year = "2000"

    noaa_data = urllib2.urlopen("ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/USW00014739.dly")
    output_file_name = "noaa_latest.csv"
    process_whole_file(first_month, first_year, noaa_data, output_file_name)
