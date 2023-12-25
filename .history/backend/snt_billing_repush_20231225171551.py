from flask import render_template, request
from datetime import datetime
import json5
import json
import requests
import re

def home():
    return render_template('snt_billing_repush.html')

