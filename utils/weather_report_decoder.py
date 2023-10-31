# Decodes a morse weather report to ship callsign, longitude and latitude

# The part before DE is the station to which is being reported 
stations = {
    "RMP": "Kaliningrad (Baltic Sea Fleet)",
    "RCV": "Sevastopol (Black Sea Fleet)",
    "RKN": "Astrakhan (Caspian Flotilla)",
    "RJS": "Vladivostok (Pacific Fleet)"
    # There are more but we'll decode the rest as 'other'
}

def get_station(morse_string):
    # Check the first part of the string, focusing on character 4 to 40
    # The station should be repeated here a few times, probably starting at the 4th character
    string_start = morse_string[4:40]
    station_probably = string_start[0:2]
    if station_probably in stations:
        return stations[station_probably]
    else:
        # Check the full string start if somewhere it includes a station
        for station_code in stations:
            if station_code in string_start:
                return stations[station_code]

# The callsign of the ship can be seen right after the DE part
# TODO: Implement a callsign dictionary here (preferably with an external file)
callsigns = {

}

def get_callsign(morse_string):
    # The callsign should appear after the DE part
    if 'DE' in morse_string:
        split_string = morse_string.split('DE')[1]
        # Get the first four characters
        callsign = split_string[:4]
        return callsign
    else: 
        return "Unknown"

# After the 99, we have the latitude and longitide
# In the format 99LLL, where the LLL is the latitude in two numbers and one decimal
# And after that QXLLL, Where Q is the globe quadrant and LLL the longitude in two numbers and once decimal
def parse_position(position_string):
    if(len(position_string) != 10):
        return "Position unknown"
    # Get the first five characters, which are the latitude
    latitude_string = position_string[:5]
    # Get the last five characters, which are the longitude
    longitude_string = position_string[5:]
    print(f"Latitude string: {latitude_string}, longitude string: {longitude_string}")
    # Get characters 3 and 4, a dot and character 5, to get the latitude
    latitude = float(latitude_string[2:4] + '.' + latitude_string[4])
    # Get the first character, which is the globe quadrant
    globe_quadrant = longitude_string[0]
    # Get characters 3 and 4, a dot and character 5, to get the longitude
    longitude = float(longitude_string[2:4] + '.' + longitude_string[4])

    return [latitude, longitude]

def get_position(morse_string):
    # Find the part of the string that starts with 99 
    # If there is no 99 in the morse_string find a part that has 10 surrounded by three numbers on both sides
    # The part we need is the 10 numbers starting with 99, or the 5 numbers before 10, 10 and the three numbers after 10
    position_string = ""
    has_99 = '99' in morse_string
    has_10 = '10' in morse_string
    if(has_99):
        # The 99 is the start of the position string, which totals 10 characters
        position_string = morse_string[morse_string.index('99'):morse_string.index('99') + 10]
    elif(has_10):
        # Find all instances of 10 in the string
        tens = [i for i in range(len(morse_string)) if morse_string.startswith('10', i)]
        for ten in tens:
            # Check if the three characters before and after are numbers
            if morse_string[ten - 3:ten].isnumeric() and morse_string[ten + 2:ten + 5].isnumeric():
                # If so, check if one of the five characters before the ten is a 9
                if "9" in morse_string[ten - 5:ten]:
                    # If so, we found the position string
                    position_string = morse_string[ten - 5:ten + 5]
                    break
    print(f"Position string: {position_string}")
    # Parse the position string
    position = parse_position(position_string)
    return position


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


def decode_report(morse):
    morse_string = morse.replace(' ', '')
    print(f"Concatenated morse string: {morse_string}")
    station = get_station(morse_string)
    callsign = get_callsign(morse_string)
    position = get_position(morse_string)

    return {
        "station": station,
        "callsign": callsign,
        "position": position
    }

# Check with dummy string
test_string = "VVV RMP RMP RMP D E RMIK RMIK Q S A ? Q TC K RMI K 5 6 0 1 6 10 1 5 0 2 5 6 0 = S ML F O R R C D 8 8 RI O 8 0 = 1 0 1 2 1 E 9 5 5 0 1019 6 4 2 4 9 8 00 7 04 100 T 9 40241 5 7 006 8 0 5 00 2 2 2 6 1 0005 8 20 3 01 10012 = A R RMI A K RMI K O K QR U K"
print(decode_report(test_string))

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