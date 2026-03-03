# family_tree.py
# cs562 - spring 2026
# valarie trinh (undergraduate)
# assignment 01 - family tree
# claude.ai was used for concept explanation, code review, and debugging

"""family tree: generates and queries a multi-generation family from csv demographic data."""

import csv
import random
import math

class Person:
    """a single person with name, birth/death years, optional partner, and children."""

    def __init__(self, first_name, last_name, year_born, year_died, gender):
        """initialize a person with name, birth/death years, and gender."""
        self._first_name = first_name
        self._last_name = last_name
        self._year_born = year_born
        self._year_died = year_died
        self._gender = gender
        self._partner = None
        self._children = []

    def get_first_name(self):
        """return the person's first name."""
        return self._first_name
    
    def get_last_name(self):
        """return the person's last name."""
        return self._last_name
    
    def get_year_born(self):
        """return the year the person was born."""
        return self._year_born
    
    def get_year_died(self):
        """return the year the person died."""
        return self._year_died
    
    def get_gender(self):
        """return the person's gender."""
        return self._gender

    def get_full_name(self):
        """return the person's full name (first and last)."""
        return f"{self._first_name} {self._last_name}"


    def get_partner(self):
        """return the person's partner, or None if none."""
        return self._partner
    
    def set_partner(self, partner):
        """set this person's partner."""
        self._partner = partner
    
    def get_children(self):
        """return the list of this person's children."""
        return self._children
    
    def add_child(self, child):
        """add a child to this person's list of children."""
        self._children.append(child)


class PersonFactory:
    """creates person instances using data loaded from csv files."""

    def __init__(self):
        """initialize empty caches for csv data."""
        self._life_expectancy = {}
        self._first_names = {}
        self._last_names = {}
        self._rank_to_probability = []
        self._birth_marriage_rates = {}
        self._gender_name_probability = {}


    def read_files(self):
        """load all csv data into memory from the default files."""
        self._read_life_expectancy()
        self._read_first_names()
        self._read_last_names()
        self._read_rank_to_probability()
        self._read_birth_marriage_rates()
        self._read_gender_name_probability()

    def create_person(self, year_born, last_name=None):
        """create a person with random name and gender and lifespan for the given birth year."""
        gender = self._pick_gender(year_born)
        first_name = self._pick_first_name(year_born, gender)

        if last_name is None:
            last_name = self._pick_last_name(year_born)

        year_died = self._calculate_year_died(year_born)
        person = Person(first_name, last_name, year_born, year_died, gender)
        return person

    def _read_life_expectancy(self):
        """load life expectancy by year from life_expectancy.csv."""
        with open('life_expectancy.csv', newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                self._life_expectancy[int(row['Year'])] = float(row['Period life expectancy at birth'])
            
    def _read_first_names(self):
        """load first names by decade and gender from first_names.csv."""
        with open('first_names.csv', newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                key = (row['decade'], row['gender'])

                if key not in self._first_names:
                    self._first_names[key] = []

                self._first_names[key].append((row['name'], float(row['frequency'])))
    
    def _read_last_names(self):
        """load last names by decade from last_names.csv."""
        with open('last_names.csv', newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                key = row['Decade']

                if key not in self._last_names:
                    self._last_names[key] = []

                self._last_names[key].append(row['LastName'])

    def _read_rank_to_probability(self):
        """load rank-to-probability weights from rank_to_probability.csv."""
        with open('rank_to_probability.csv', newline="") as file:
            reader = csv.reader(file)

            for row in reader:
                raw = [float(x) for x in row]
                total = sum(raw)
                self._rank_to_probability = [x / total for x in raw]

    def _read_birth_marriage_rates(self):
        """load birth and marriage rates by decade from birth_and_marriage_rates.csv."""
        with open('birth_and_marriage_rates.csv', newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                self._birth_marriage_rates[row['decade']] = {
                    'birth_rate': float(row['birth_rate']),
                    'marriage_rate': float(row['marriage_rate'])
                }
            
    def _read_gender_name_probability(self):
        """load gender probability by decade from gender_name_probability.csv."""
        with open('gender_name_probability.csv', newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:

                if row['decade'] not in self._gender_name_probability:
                    self._gender_name_probability[row['decade']] = {}

                self._gender_name_probability[row['decade']][row['gender']] = float(row['probability'])


    def _year_to_decade(self, year):
        """convert a birth year to a decade string (e.g. 1985 -> '1980s')."""
        return f"{year // 10}0s"


    def _pick_gender(self, year_born):
        """pick a gender at random using decade-specific probabilities."""
        decade = self._year_to_decade(year_born)
        probability = self._gender_name_probability[decade]
        return random.choices(list(probability.keys()), list(probability.values()))[0]

    def _pick_first_name(self, year_born, gender):
        """pick a first name at random for the birth year (gender and frequency weighted)."""
        decade = self._year_to_decade(year_born)
        key = (decade, gender)
        names = self._first_names[key]
        return random.choices(names, [x[1] for x in names])[0][0]

    def _pick_last_name(self, year_born):
        """pick a last name at random for the birth decade using rank probabilities."""
        decade = self._year_to_decade(year_born)
        return random.choices(self._last_names[decade], weights=self._rank_to_probability)[0]


    def _calculate_year_died(self, year_born):
        """compute a death year from life expectancy at birth year plus a random offset."""
        if year_born not in self._life_expectancy:
            candidates = [y for y in self._life_expectancy if y <= year_born]
            year_born = max(candidates) if candidates else min(self._life_expectancy)
        expectancy = self._life_expectancy[year_born]
        offset = random.uniform(-10, 10)
        return round(year_born + expectancy + offset)

    def get_marriage_rate(self, year_born):
        """get the marriage rate for the given birth year."""
        decade = self._year_to_decade(year_born)
        return self._birth_marriage_rates[decade]['marriage_rate']


class FamilyTree:
    """holds a set of people and founders and connects them through generation and queries."""

    def __init__(self):
        """initialize the family tree with a person factory and empty people lists."""
        self._person = PersonFactory()
        self._all_people = set()
        self._founders = []

    def generate(self):
        """load csv data, create founder couple, and recursively generate their descendants."""
        print("reading files...")
        self._person.read_files()
        print("generating family tree...")

        founder_one = self._person.create_person(1950, "Jones")
        founder_two = self._person.create_person(1950, "Jones")

        founder_one.set_partner(founder_two)
        founder_two.set_partner(founder_one)

        self._add_person(founder_one)
        self._add_person(founder_two)

        self._founders.append(founder_one)
        self._founders.append(founder_two)

        self._generate_children(founder_one, "Jones")

    def _add_person(self, person):
        """add a person to _all_people (set prevents duplicates)."""
        self._all_people.add(person)

    def _generate_children(self, parent, last_name):
        """generate children for the given parent."""
        year_born = parent.get_year_born()
        decade = self._person._year_to_decade(year_born)
        birth_rate = self._person._birth_marriage_rates[decade]['birth_rate']
        min_children = math.ceil(birth_rate - 1.5)
        max_children = math.ceil(birth_rate + 1.5)
        num_children = random.randint(min_children, max_children)

        if num_children == 0 or year_born >= 2120:
            return
        
        child_start = int(year_born) + 25
        child_end = int(year_born) + 45

        if num_children == 1:
            child_years = [random.randint(child_start, child_end)]
        else:
            gap = (child_end - child_start) / (num_children - 1)
            child_years = [round(child_start + i * gap) for i in range(num_children)]

        for child_year in child_years:
            if child_year > 2120:
                break
            child_person = self._person.create_person(child_year, last_name)
            parent.add_child(child_person)
            self._add_person(child_person)

            if random.random() < self._person.get_marriage_rate(child_year):
                partner_year = child_year + random.randint(-10, 10)
                partner = self._person.create_person(partner_year)
                child_person.set_partner(partner)
                partner.set_partner(child_person)
                self._add_person(partner)

            self._generate_children(child_person, last_name)
    
    def query_total(self):
        """query the total number of people in the family tree."""
        print(f"this tree has {len(self._all_people)} people total")

    def query_by_decade(self):
        """query the number of people born in each decade."""
        decade_counts = {}
        for person in self._all_people:
            decade = (person.get_year_born() // 10) * 10
            if decade not in decade_counts:
                decade_counts[decade] = 0
            decade_counts[decade] += 1

        for decade in sorted(decade_counts):
            print(f"{decade}s: {decade_counts[decade]} people")

    def query_duplicate_names(self):
        """query the number of people with duplicate names."""
        name_counts = {}
        for person in self._all_people:
            name = person.get_full_name()

            if name not in name_counts:
                name_counts[name] = 0
            
            name_counts[name] += 1

        duplicates = [name for name, count in name_counts.items() if count > 1]
        print(f"there are {len(duplicates)} people with duplicate names")
        for name in duplicates:
            print(f"* {name}: {name_counts[name]} people")


    def run(self):
        """generate the family tree and run the interactive query menu until the user exits."""
        self.generate()

        while True:
            print("are you interested in:")
            print("1. total number of people in the tree")
            print("2. number of people born in each decade")
            print("3. number of people with duplicate names")
            print("4. exit")
            
            try:
                choice = int(input("enter your choice: "))
                if choice == 1:
                    self.query_total()
                elif choice == 2:
                    self.query_by_decade()
                elif choice == 3:
                    self.query_duplicate_names()
                elif choice == 4:
                    break
                else:
                    print("invalid choice")
            except ValueError:
                print("please enter a number between 1 and 4")
        
if __name__ == "__main__":
    tree = FamilyTree()
    tree.run()