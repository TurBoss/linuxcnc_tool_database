# coding=utf-8
#   2022 TurBoss

from pprint import pprint
from deepdiff import DeepDiff
from sqlalchemy.sql import exists

from tool_db.base import Session, engine, Base
from tool_db.tool_database import Spindles, Magazines, Pockets, GeomGroups, Geometries, Offsets, Tools


class ToolDBHandler:
    """Tool Database Handler
    
    """
    
    def __init__(self):
        
        Base.metadata.create_all(engine)

        self.session = Session()
        
        print("Session open.")

    #
    # Spindles Actions
    #

    def new_spindle(self, description, active):
        
        print(f"new spindle {description}")
        
        spindle_offsets = Offsets(
            description="spindle default values",
        )
        
        spindle = Spindles(
            description=description,
            active=active
        )
        
        spindle.offsets = [spindle_offsets]
        
        self.session.add(spindle)
        self.session.add(spindle_offsets)
        
        try:
            self.session.commit()
            print("spindle created.")

            
        except Exception as e:
            print(e)

        # finally:
        #     session.close()
        

    def edit_spindle(self):
        pass
    
    def delete_spindle(self):
        pass

    #
    # Magazines Actions
    #

    def new_magazine(self, description, type, num_pockets=12):
        
        print(f"new magazine, {description}")
        
        magazines = Magazines(
            description=description,
            type=type,
            num_pockets=num_pockets
        )

        self.session.add(magazines)
        
        try:
            self.session.commit()
            print("magazine created.")
            
        except Exception as e:
            print(e)

        # finally:
        #     session.close()

    def edit_magazine(self):
        pass
    
    def delete_magazine(self):
        pass

    #
    # Pockets Actions
    #

    def new_pocket(self, tool_db_handler, pocket_offs=None, slot_pos=None):
               
        pocket_exist = self.session.query(exists().where(Pockets.slot_pos == slot_pos)).scalar()
        
        if pocket_exist:
            print(f"pocket in slot {slot_pos} already exist")
            return 
        
        pocket = Pockets(
            pocket_offs=pocket_offs,
            slot_pos=slot_pos,
            magazines_id=tool_db_handler
            
        )
        
        
        self.session.add(pocket)
        
        try:
            self.session.commit()
            print(f"pocket {slot_pos} created.")
            
        except Exception as e:
            print(e)

        # finally:
        #     session.close()
        

    def edit_geometries(self):
        pass
    
    def delete_geometries(self):
        pass

    #
    # Geometries Actions
    #

    def new_geometry(self, description, orientation=None, frontangle=None, backangle=None):
        
        geometries = Geometries(
            description=description,
            orientation=orientation,
            frontangle=frontangle,
            backangle=backangle
        )

        self.session.add(geometries)
        
        try:
            self.session.commit()
            print(f"geometry {description} created.")
            
        except Exception as e:
            print(e)

        # finally:
        #     session.close()
        

    def edit_geometries(self):
        pass
    
    def delete_geometries(self):
        pass

    #
    # Offsets Actions
    #

    def new_offsets(self, description, number, tool_id=None, spindle_id=None):
       
        offsets = Offsets(
            description=description,
            number=number,
            tool_id=tool_id,
            spindle_id=spindle_id
        )

        self.session.add(offsets)
        
        try:
            self.session.commit()
            print(f"Tool number {number} created")
            
        except Exception as e:
            print(e)

        # finally:
        #     session.close()

    def edit_offsets(self):
        pass
    
    def delete_offsets(self):
        pass
    #
    # Tools Actions
    #

    def new_tool(self, description, number, magazine=1):
        
        tool_exist = self.session.query(exists().where(Tools.number == number)).scalar()
        
        if tool_exist:
            print(f"tool with munber {number} already exist")
            return
        
        tool_offsets = Offsets(
            description="tool default values",
        )
        tool = Tools(
            description=description,
            number=number,
            magazines_id=magazine
        )
        
        tool.offsets = [tool_offsets]
        
        # diff = DeepDiff(tool_exist, tool, view="tree")
        #
        # pprint(diff)
        #
        # to_insert = diff.get("dictionary_item_added")
        # to_update = diff.get("values_changed")
        # to_delete = diff.get("dictionary_item_removed")
        #
        # print(to_insert)
        # print(to_update)
        # print(to_delete)
        
        self.session.add(tool)
        self.session.add(tool_offsets)
        
        try:
            self.session.commit()
            print(f"Tool number {number} created")
            
        except Exception as e:
            print(e)

        # finally:
        #     session.close()

    def edit_tool(self):
        pass
    
    def delete_tool(self):
        pass


def main():
    
    tool_db_handler = ToolDBHandler()
    
    tool_db_handler.new_geometry("default geometry")
    
    tool_db_handler.new_magazine("Main magazine", "linear", 12)

    for i in range(1, 12 + 1):
        tool_db_handler.new_pocket(1, None, i)

    tool_db_handler.new_spindle("Main spindle", True)
    
    for i in range(1, 30+1):
        tool_db_handler.new_tool("Tool {i}", i)

if __name__ == "__main__":
    main()
