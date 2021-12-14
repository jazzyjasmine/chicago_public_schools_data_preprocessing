import math
import csv
import webbrowser

EARTH_RADIUS = 3961


class Coordinate:
    def __init__(self, latitude, longitude):
        """
        Constructor of an instance of Coordinate

        :param latitude: (float) latitude of the physical location in radians
        :param longitude: (float) longitude of the physical location in radians
        """
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        """
        Returns a string as a representation of a Coordinate

        :return: (string) a string as a representation of a Coordinate
        """
        return "Coordinate: (latitude(radians): {}, longitude(radians): {})".format(self.latitude, self.longitude)

    @classmethod
    def fromdegrees(cls, latitude, longitude):
        """
        Alternate constructor of an instance of Coordinate: takes in location in degrees and create a Coordinate instance

        :param latitude: (float) latitude of the physical location in degrees
        :param longitude: (float) longitude of the physical location in degrees
        :return: (Coordinate) an instance of Coordinate (with latitude and longitude in radians)
        """
        return cls(Coordinate.degree_to_radian(latitude), Coordinate.degree_to_radian(longitude))

    @staticmethod
    def degree_to_radian(degree_latitude_or_longitude):
        """
        Turns a degree formatted latitude/longitude into a radian formatted latitude/longitude

        :param degree_latitude_or_longitude: (float) a degree formatted latitude/longitude
        :return: (float) a radian formatted latitude/longitude
        """
        radian_latitude_or_longitude = degree_latitude_or_longitude * math.pi / 180
        return radian_latitude_or_longitude

    def distance(self, coord):
        """
        Accepts another instance of Coordinate and calculate the distance in miles to it from the current instance.
        (way to calculate distance: https://en.wikipedia.org/wiki/Haversine_formula)

        :param coord: (Coordinate) an instance of Coordinate used to calculate the distance
        :return: (float) the distance in miles to it from the current instance
        """
        latitude_diff = self.latitude - coord.latitude
        longitude_diff = self.longitude - coord.longitude
        return 2 * EARTH_RADIUS * math.asin(math.sqrt(
            math.pow(math.sin(latitude_diff / 2), 2) + math.cos(self.latitude) * math.cos(coord.latitude) * math.pow(
                math.sin(longitude_diff / 2), 2)))

    def as_degrees(self):
        """
        Takes a Coordinate and returns a tuple of the latitude and longitude in degrees.

        :return: (tuple) a tuple of the latitude and longitude in degrees
        """
        degree_latitude = self.latitude * 180 / math.pi
        degree_longitude = self.longitude * 180 / math.pi
        return degree_latitude, degree_longitude

    def show_map(self):
        """
        Opens up Google Maps in a web browser with a point placed on the latitude/longitude of the coordinate

        No return value.
        """
        webbrowser.open('http://maps.google.com/maps?q={}'.format(Coordinate.as_degrees(self)))


class School:
    def __init__(self, data):
        """
        Constructor of an instance of School

        :param data: (dict) a dictionary corresponding to a row of the "schools.csv" file
        """
        self.id = int(data["School_ID"])
        self.name = data["Short_Name"]
        self.network = data["Network"]
        self.address = data["Address"]
        self.zip = data["Zip"]
        self.phone = data["Phone"]
        self.grades = data["Grades"].split(", ")
        self.location = Coordinate.fromdegrees(float(data["Lat"]), float(data["Long"]))

    def __repr__(self):
        """
        Returns a multiline string as a representation of a School

        :return: a multiline string as a representation of a School
        """
        return "======School====== \nid: {},\nname: {},\nnetwork: {},\naddress: {},\nzip: {},\nphone: {}," \
               "\ngrades: {}," \
               "\nlocation: {} \n".format(self.id, self.name, self.network, self.address, self.zip, self.phone,
                                          self.grades, Coordinate.__repr__(self.location))

    def distance(self, coord):
        """
        Accepts another instance of Coordinate and calculate the distance in miles to it from the current school.
        (way to calculate distance: https://en.wikipedia.org/wiki/Haversine_formula)

        :param coord: (Coordinate) an instance of Coordinate used to calculate the distance
        :return: (float) the distance in miles to it from the current school
        """
        latitude_diff = self.location.latitude - coord.latitude
        longitude_diff = self.location.longitude - coord.longitude
        return 2 * EARTH_RADIUS * math.asin(math.sqrt(
            math.pow(math.sin(latitude_diff / 2), 2) + math.cos(self.location.latitude) * math.cos(
                coord.latitude) * math.pow(
                math.sin(longitude_diff / 2), 2)))

    def full_address(self):
        """
        Displays the full address of a school

        :return: (string) multi-line string of street address, city, state, and ZIP code of the school.
        """
        return "{} \nChicago, IL \n{}".format(self.address, self.zip)


class CPS:
    def __init__(self, filename):
        """
        Constructor of an instance of CPS

        :param filename: (string) a filename for the CSV file in which the school data is stored
        """
        self.schools = []
        with open("schools.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            header = next(csv_reader)[:]
            for line in csv_reader:
                content = line[:]
                single_school_dict = dict(zip(header, content))
                current_school = School(single_school_dict)
                self.schools.append(current_school)

    def nearby_schools(self, coord, radius=1.0):
        """
        Accepts an instance of Coordinate and returns a list of School instances that are within radius miles of the given coordinate.

        :param coord: (Coordinate) an instance of Coordinate, representing a physical position in radians
        :param radius: (float) the radius (in mile) with a center of the coordinate
        :return: (list) a list of School instances that are within radius miles of the given coordinate
        """
        nearby_schools = []
        for school in self.schools:
            current_distance = Coordinate.distance(coord, school.location)
            if current_distance > radius:
                continue
            nearby_schools.append(school)
        return nearby_schools

    def get_schools_by_grade(self, *grades):
        """
        Accepts one or more grades as strings and returns a list of School instances that teach all of the given grades.

        :param grades: (string) an arbitrary number of grades
        :return: (list) a list of School instances that teach all of the given grades
        """
        input_grades = []
        for grade in grades:
            input_grades.append(grade)
        schools_by_grade = []
        for school in self.schools:
            if not set(input_grades).issubset(set(school.grades)):
                continue
            schools_by_grade.append(school)
        return schools_by_grade

    def get_schools_by_network(self, network):
        """
        Accepts the network name as a string and returns a list of School instances in that network.

        :param network: (string) a network of school
        :return: (list) a list of School instances in the given network
        """
        schools_by_network = []
        for school in self.schools:
            if school.network != network:
                continue
            schools_by_network.append(school)
        return schools_by_network

