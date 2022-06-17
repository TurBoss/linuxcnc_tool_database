# coding=utf-8
#   2022 TurBoss
#
#   This file is part of LinuxCNC.
#
#   LinuxCNC is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   LinuxCNC is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with LinuxCNC.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite', echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()
