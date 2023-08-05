#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import sys
import json
import time
import datetime
import argparse

import click
import colorama

from impact_factor import util
from impact_factor import ImpactFactor, DEFAULT_DB, __version__, __epilog__

