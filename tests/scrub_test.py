# this allows an import from the parent directory
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from requests import get
from pprint import pprint
from battlefield import scrub


url = "https://battlefieldtracker.com/bfv/profile/origin/115GOTYOUR6/weapons"
page = get(url)
weap_stats = scrub.weaps(page, "115GOTYOUR6")

pprint(weap_stats)
