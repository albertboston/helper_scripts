import urllib2

"""
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
#answer = urllib2.urlopen("ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/USW00014739.dly")
#with open("noaa_ftp_data.dly", "w") as ftpfile:
#  for line in answer.readlines():
#    ftpfile.write(line)


elements_we_want = ["TMIN", "TMAX", "PRCP", "SNOW", "WSF2"]
# min temp, max temp, avg temp, precip, snowfall, fastest 2min wind speed

# take in a clump of month rows and turn it into 31 day rows
# month data is a dictionary from [element type] -> [list of 31 values]
def process_month_data(year, month, month_data):
  with open("my_csv_output.csv", "a+") as my_out_file:
    for day_index in range(0,31):
      a_line = []
      padded_day = format(day_index + 1, "02")
      a_line.append(year + month + padded_day)
      for element in elements_we_want:
        a_line.append(str(int(month_data[element][day_index])))
      my_out_file.write((",".join(a_line)) + "\n")

month_data = {}
last_seen_month = "01"
last_seen_year = "2000"

with open("noaa_ftp_data.dly", "r") as data_file:
  for a_line in data_file.readlines():
    my_id = a_line[0:11]
    my_year = a_line[11:15]

    # only want recent data, so skip if not after 2000
    if(int(my_year) < 2000):
      continue

    my_month = a_line[15:17]
    my_elem = a_line[17:21]

    # write out the data for the month we've been reading when we get to a new month
    # keep track of last_seen so that it makes sense
    if my_month != last_seen_month:
      process_month_data(last_seen_year, last_seen_month, month_data)
      last_seen_month = my_month
      last_seen_year = my_year
      month_data.clear()

    day_values = []

    # each line is an element - but only deal with it if we want the element
    if my_elem in elements_we_want:
      for day_index in range(0, 31):
        # math for pulling out values around the flags
        value_index = 21 + (day_index * 8) 
        day_values.append(a_line[value_index:value_index + 5])
      month_data[my_elem] = day_values

  # we've got one last month left loaded, process it
  # TODO: fix control flow so this extra process is built into the above loop
  process_month_data(last_seen_year, last_seen_month, month_data)
