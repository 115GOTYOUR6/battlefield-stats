# this allows an import from the parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from requests import get
from pprint import pprint
from battlefield import scrub

flag = 'weap'

if flag == 'weap':
    url = "https://battlefieldtracker.com/bfv/profile/origin/115GOTYOUR6/weapons"
    page = get(url)
    weap_stats = scrub.weaps(page)

    for i in weap_stats:
        print(i)
elif flag == 'over':
    url = "https://battlefieldtracker.com/bfv/profile/origin/115GOTYOUR6/overview"
    page = get(url)
    prof_stats = scrub.overview(page)

    for i in prof_stats:
        print(i)
