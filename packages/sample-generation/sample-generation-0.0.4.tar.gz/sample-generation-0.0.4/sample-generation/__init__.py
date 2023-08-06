# Required Libraries
import random
import string
import numpy as np
import time
from datetime import date
from random import randint
from datetime import datetime

from faker import Faker
fake = Faker('en_GB')
Faker.seed(0)


''' 
IDs
This function is able to produce any lenght of ID number based on input lenght
MHMDS Person ID/ MHMDS Spell ID/ patid/ pracid/ RowID/ SourceItemID/ SYSTEM_ID_E
'''
def get_id(n):
  id = ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])
  return id

'''
Code
This function is able to produce any lenght of code based on input lenght
Main Specialty code (Mental Health)/ NHS Occupation Code/ Organisation Code (Code of Commissioner)/ 
Organisation Code (Code of Provider) /ALF_STS_CD/ LSOA2001_CD/ proms_proc_code
'''
def get_code(n):
  randomstr = ''.join(random.choices(string.ascii_letters+string.digits,k = n)).upper()
  return randomstr

# Gender
# Generate array of random Genders
def get_genders(size, p=None):
  """Generate n-length ndarray of genders."""
  if not p:
      # default probabilities
      p = (0.46, 0.46, 0.07, 0.01)
  gender = ("Male", "Female", "Other", "")
  return np.random.choice(gender, size=size, p=p)

# Age (We need to know more specific age range)
def get_random_age():
  random_age = ' '.join([str(random.randint(0, 130)).zfill(1) for i in range(1)])
  return random_age

# Serial Number
# proms_serial_no /  spno/ Sponsor No/ Serial No
def serial_no():
  random_no = ''.join([str(random.randint(0, 999)).zfill(1) for i in range(2)])
  return random_no

# Ethnicity 
def get_ethnicity():
  ethnic_groups = ['English', 'Welsh', 'Scottish', 'Northern Irish or British', 'Other White background', 'White and Black Caribbean', 'White and Black African',
                'White and Asian', 'Multiple ethnic background', 'Indian', 'Bangladeshi', 'Pakistani', 'Chinese', 'Other Asian Background', 'African', 'Caribbean',
                'Arab', 'Other Black, African or Caribbean background', 'Arab', 'Any other ethnic group']
  rand_ethnicity = random.choice(ethnic_groups)
  return rand_ethnicity

# Location 
# Generates only random country
def get_country():
  return fake.country()

# Postcode
def get_UK_postcode():
  postcode = fake.postcode()
  return postcode

# Profession
# Job role
def get_job_role():
  return fake.job()

# Date
def get_date(start, end, prop):
  def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))
  return str_time_prop(start, end, '%d/%m/%Y', prop)


print('Random Date:', get_date("1/1/2008", datetime.now().strftime("%d/%m/%Y"), random.random()))

print(f'Patient ID: {get_id(10)}\nCode: {get_code(10)}\nGender: {get_genders(1)}\nAge: {get_random_age()}\
      \nSerial No: {serial_no()}\nEthnicity: {get_ethnicity()}\nCountry: {get_country()}\nUK postcode: {get_UK_postcode()}\
      \nCountry: {get_job_role()}')