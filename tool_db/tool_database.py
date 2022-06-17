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

# Implementation of Andy Pugh page at https://wiki.linuxcnc.org/cgi-bin/wiki.pl?ToolDatabase

from sqlalchemy import Column, Date, Table, ForeignKey, Boolean, Integer, Integer, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import Choice, ChoiceType
from .base import Base


class Spindles(Base):
    """The "Spindles" table.
    
    The "id" is a unique identifier for every "spindle" that has access to the tools in the database.
    An optional text "description" is available to clarify things for the user, but is not used by the system.
    "machine_id" indicates which machine the spindle is mounted on,
    "active" shows whether the spindle is the currently-active one (as G-code has no way to differentiate between spindles in multi-spindle machines).
    "tool_id" shows which tool is currently mounted in the spindle. A value of zero indicates that no tool is loaded.
    The "offset_id" is a key to an optional spindle offset which will be added to each tool offset.
    The purpose of this is to compensate for any differences in engagement depth for the same tool in multiple spindles.
    This is probably only relevant to situations where multiple spindles share an axis, as typically this delta would be subsumed into the axis offsets.
    It is intended that the "spindle_hrs" timer will be automatically updated by LinuxCNC. 
    """
    
    __tablename__ = 'spindles'
    
    id = Column(Integer, primary_key=True)
    
    description = Column(Text)
    
    # machine_id = Column(Text, ForeignKey('machine.id'))
    active = Column(Boolean, default=True)
    # tool_id = Column(Integer, default=None)
    spindle_hrs = Column(Float, default=0.0)
    
    # DB relationships betwen Tools table
    
    tools = relationship("Tools", back_populates="spindles")

    # DB relationships betwen Offsets table
    
    offsets = relationship("Offsets", back_populates="spindles")


class Magazines(Base):
    """The "Magazines" table.
    
    The concept of a tool magazine is a new introduction in this iteration of the tool table.
    It is a way to indicate which subset of all tools are currently available to any particular spindle.
    This may refer to an actual physically-interchangable tool carousel, or could also be used to encode job-specific setups in a single carousel.
    In the latter case switching between tool selections only involves changing the magazine number, rather than editing the entire tool table. 
    As well as encoding tool-to-spindle availability this table contains data of use to toolchanger code. The "base_pos" position is a key to a position where the base tool can be found (q.v. "offsets") 
    """
    
    TYPES = [
        ("rotary", "Rotary"),
        ("linear", "Linear")
    ]
    
    __tablename__ = 'magazines'
    
    id = Column(Integer, primary_key=True)
    
    description = Column(Text, default="")
    
    type = Column(ChoiceType(TYPES))
    num_pockets = Column(Integer, default=1)
    base_pos = Column(Integer)
    
    # DB relationships betwen Pockets table
    
    pockets = relationship("Pockets", back_populates="magazines")
    
    # DB relationships betwen Tools table
    
    tools = relationship("Tools", back_populates="magazines")


class Pockets(Base):
    """The "Pockets" table.
    
    This structure is keyed on magazine/pocket/tool to support the possibility of the same physical tool appearing several times in a number of setups,
    either in the same or different physical pockets. The "slot_pos" is an offset from the base position for the physical pocket for use by such systems as rack toolchangers,
    or as the A-position, if for example, a rotary axis was being used as a tool turret. The pocket_offs is intended to encode the fact that
    individual slots in a turret-style changer on a lathe might place the same physical tool in a slightly different location. 
    """
    
    __tablename__ = 'pockets'
    
    id = Column(Integer, primary_key=True) # id primary keys cant default to 0
    
    pocket_offs = Column(Integer, default=None)
    slot_pos = Column(Integer, default=None)
    
    # DB relationships betwen Magazines table
    
    magazines_id = Column(Integer, ForeignKey('magazines.id'))
    magazines = relationship("Magazines", back_populates="pockets")
    
    # DB relationships betwen Tools table
    
    tools_id = Column(Integer, ForeignKey('tools.id'))
    tools = relationship("Tools", back_populates="pockets")


class GeomGroups(Base):
    """The "GeomGroups" table.
    
    This table groups together an arbitrary number of tool, spindle, turret or slot offsets to allow compound offsets to be defined.
    This allows for G-code to refer to composite offsets by a single integer value (for example in G43 Hnn or G10 L2 Pnn).
    The intention is that when searching for an offset by name, that the initial search will be of the ID numbers in this table,
    and then if the ID number is not found, then the individual offsets will be searched.
    Thus if the individual offsets have ID numbers distinct from the offset groups, is it possible to also access individual sub-offsets, such as wear. 
    """
    
    __tablename__ = 'geom_groups'

    id = Column(Integer, primary_key=True)
    
    description = Column(Text, default="", primary_key=True)
    
    offset_id = Column(Integer, default=True)
    geom_id = Column(Integer, default=None)


class Geometries(Base):
    """The "Geometries" table.
        
    This table holds the non motion-related aspects of a given tool, such as the physical tool shape.
    The data in this table is likely to be only used by GUIs or visualisation tools. 
    """
    
    __tablename__ = 'geometries'

    id = Column(Integer, primary_key=True)
        
    description = Column(Text, default="")
    
    orientation = Column(Integer, default=None)
    frontangle = Column(Float, default=None)
    backangle = Column(Float, default=None)
    
    # DB relationships betwen Tools table
    
    tools = relationship("Tools", back_populates="geometries")


class Offsets(Base):
    """The "Offsets" table.
    
    This table contains the list of physical offsets.
    The numbers in this table are in the units defined in the "metadata" table. 
    """
    
    __tablename__ = 'offsets'
    
    id = Column(Integer, primary_key=True)
    
    description = Column(Text, default="")
    
    x_offset = Column(Float, default=0.0)
    y_offset = Column(Float, default=0.0)
    z_offset = Column(Float, default=0.0)
    a_offset = Column(Float, default=0.0)
    b_offset = Column(Float, default=0.0)
    c_offset = Column(Float, default=0.0)
    u_offset = Column(Float, default=0.0)
    v_offset = Column(Float, default=0.0)
    w_offset = Column(Float, default=0.0)
    diameter = Column(Float, default=0.0)
    
    # DB relationships betwen Tools table
    
    tools_id = Column(Integer, ForeignKey('tools.id'))
    tools = relationship("Tools", back_populates="offsets")
    
    # DB relationships betwen Spindles table
    
    spindles_id = Column(Integer, ForeignKey('spindles.id'))
    spindles = relationship("Spindles", back_populates="offsets")


class Tools(Base):
    """The "Tools" table.
     
    This table associates a physical tool with its offsets and geometry.
    It also defines what "number" the tool can be called up by.
    One feature of this tool table schema is that it is possible to have several physical tools all of the same type,
    and the system (by means of sql search queries) can choose between them on the basis of such factors as least-wear,
    closest in the tool-chain or other factors.
    """
        
    __tablename__ = 'tools'
    
    id = Column(Integer, primary_key=True)
    
    description = Column(Text, default="")
    
    number = Column(Integer)
    spindle_hrs = Column(Float, default=0.0)
    distance = Column(Float, default=0.0)
    in_use = Column(Boolean, default=True)
    max_rpm = Column(Float, default=-1)
    
    # DB relationships betwen Pockets table
    
    pockets = relationship("Pockets", back_populates="tools")
    
    # DB relationships betwen Geometries table
    
    geometries_id = Column(Integer, ForeignKey('geometries.id'))
    geometries = relationship("Geometries", back_populates="tools")
    
    # DB relationships betwen Magazines table
    
    magazines_id = Column(Integer, ForeignKey('magazines.id'))
    magazines = relationship("Magazines", back_populates="tools")
    
    # DB relationships betwen Offsets table
    
    offsets = relationship("Offsets", back_populates="tools")
    
    # DB relationships betwen Spindles table
    
    spindles_id = Column(Integer, ForeignKey('spindles.id'))
    spindles = relationship("Spindles", back_populates="tools")
