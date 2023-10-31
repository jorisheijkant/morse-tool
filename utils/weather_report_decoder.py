# Decodes a morse weather report to ship callsign, longitude and latitude

# The part before DE is the station to which is being reported 
stations = {
    "RMP": "Kaliningrad (Baltic Sea Fleet)",
    "RCV": "Sevastopol (Black Sea Fleet)",
    "RKN": "Astrakhan (Caspian Flotilla)",
    "RJS": "Vladivostok (Pacific Fleet)"
    # There are more but we'll decode the rest as 'other'
}

# The callsign of the ship can be seen right after the DE part
# TODO: Implement a callsign dictionary here (preferably with an external file)
callsigns = {

}

# After the 99, we have the latitude and longitide
# In the format 99LLL, where the LLL is the latitude in two numbers and one decimal
# And after that QXLLL, Where Q is the globe quadrant and LLL the longitude in two numbers and once decimal
def parse_position(position_string):
    #TODO: Build some more conditions here to prevent crashing and key errors
    latitude_string = position_string.split(' ')[0]
    longitude_string = position_string.split(' ')[1]
    latitude = float(latitude_string[3] + ',' + latitude_string[:2])
    longitude = float(longitude_string[3] + ',' + longitude_string[:2])

    return [latitude, longitude]

# The speed and direction of the ship is shown after the 222 part in the code
# In the format of 222CS, where C is the coarse and S is the speed
coarse_dictionary = {
    "0": "Ship hoves to",
    "1": "NE",
    "2": "E",
    "3": "SE",
    "4": "S",
    "5": "SW",
    "6": "W",
    "7": "NW",
    "8": "N",
    "9": "Unknown/not reported"
}

speed_dictionary = {
    "0": "0 knots",
    "1": "1 to 5 knots",
    "2": "6 to 10 knots",
    "3": "11 to 15 knots",
    "4": "16 to 20 knots",
    "5": "21 to 25 knots",
    "6": "26 to 30 knots",
    "7": "31 to 35 knots",
    "8": "36 to 40 knots",
    "9": "Not reported / Over 40 knots"
}

# Q codes that are used in weather reports
###
# QTC I have a message (message follows)
# QWH I start send on frequency (KHz)
# QWH 9700/rptd = 12056/rptd will send on 9700, alternatively on 12056
# QWH 9700/8536 = 12056/12572 the link will run with two parallel frequencies
# QYR I start working on 81 Baud RTTY (presumed)
# QYS I start working on duplex RTTY
# QYT4 I start use MS-5 system
# QYT4 QMO adjust your MS-5 system
# QSX I will listen on frequency (KHz)
# QSX 8440/rptd = 12414/rptd I will listen on 8440, alternatively on 12414
# QLS use (upper) alternative frequency or change frequency
# QRS send slower
# QCM your transmission is affected by technical problems
# QLN  rpt via landline
# QSA radio check (request and reply)