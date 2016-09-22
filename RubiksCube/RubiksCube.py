import random

class Tile():
    """Color and Tile are integers. When printing, 
    the integers are used as indices for their respective name lists."""
    def __init__(self, color, orientation):
        self.color=color
        self.orientation=orientation
        self.middle_orientation=''
    def __str__(self):
        return color_names[self.color] + 'facing' + orientation_names[self.orientation]
    color_names=['W','Y','R','O','B','G']
    orientation_names=['Front','Back','Right','Left','Up','Down']
    color_opposites={0:1, 1:0, 2:3, 3:2, 4:5, 5:4}

class Cube():
    """Cube is a composition of Tile(s) having the same position.
    Type is an integer declared when generating a Solved Cube
    and represents the number of tiles in the cube."""
    def __init__(self, position, type=0):
        self.tiles=[]
        self.position=position
        self.type=type
        self.solved=False
    type_names=[None,'Middle','Edge','Corner']
    #           This is how positions change. Each face value(int) is mapped to specific positions.
    #       Each 90 degree clockwise turn moves a cube's position two spots to the right. More accurately,
    #       the index of the cube's position changes by +2 and -2 for counter-clockwise turns.
    move_face_positions={2:(3,12,21,24,27,18,9,6),#Right
                   3:(19,10,1,4,7,16,25,22),#Left
                   6:(2,5,8,17,26,23,20,11),#Middle
                   4:(19,20,21,12,3,2,1,10),#Up
                   5:(7,8,9,18,27,26,25,16),#Down
                   7:(4,5,6,15,24,23,22,13),#Equator
                   0:(1,2,3,6,9,8,7,4),#Front
                   1:(21,20,19,22,25,26,27,24),#Back
                   8:(10,11,12,15,18,17,16,13)}#Side
    move_orientation={0:[4,2,5,3], 1:[3,5,2,4], 8:[4,2,5,3],
                      2:[0,4,1,5], 3:[5,1,4,0], 6:[5,1,4,0],
                      4:[3,1,2,0], 5:[0,2,1,3], 7:[0,2,1,3], }

def index_change(current, change, length):
    """current=current index        change=amount of index places to move       length=len(list)
    Returns index."""
    i=current+change
    if i>length-1: i -=length
    if i<0: i +=length
    return i
def shortest_distance(ic,id,step):
    """ic=current index of cube     id=desired index of cube
    Finds shortest turn for moving a cube to a certain position. 
    Returns (multiple, counter bool)."""
    d=id-ic
    return abs(d/step),d<0
def find_edge_position_intersect(orientation1, orientation2):
    """Returns the edge position that intersects two orientations."""
    s1=set(Cube.move_face_positions[orientation1])
    s2=set(Cube.move_face_positions[orientation2])
    si=s1.intersection(s2)
    for common in si:
        if common%2==0:
            return common
def find_corner_position_intersect(orientation1, orientation2, orientation3):
    """Returns the corner position that intersects three orientations."""
    s1=set(Cube.move_face_positions[orientation1])
    s2=set(Cube.move_face_positions[orientation2])
    s3=set(Cube.move_face_positions[orientation3])
    si=s1.intersection(s2,s3)
    return si.pop()
def is_solved(cubes):
    """Returns bool of whether the list of cubes are solved.
    Cubes=list of """
    for cube in cubes:
        for tile in cube.tiles:
            if tile.orientation!=tile.middle_orientation:
                return False
    return True


class Rubiks():
    """Generates a solved Rubik's Cube composed of other cubes."""
    #           Used in generating a solved cube. Each position is mapped to values, 
    #       one for each tile in the position. Each value is used to create a tile with
    #       its color and orientation set to the value.
    solved_position_indices={1: [0, 3, 4], 2: [0, 4], 3: [0, 2, 4], 4: [0, 3], 5: [0], 6: [0, 2], 
                            7: [0, 3, 5], 8: [0, 5], 9: [0, 2, 5], 10: [3, 4], 11: [4], 12: [2, 4], 
                            13: [3], 15: [2], 16: [3, 5], 17: [5], 18: [2, 5], 19: [1, 3, 4], 
                            20: [1, 4], 21: [1, 2, 4], 22: [1, 3], 23: [1], 24: [1, 2], 25: [1, 3, 5], 
                            26: [1, 5], 27: [1, 2, 5]}
    move_names=['Front','Back','Right','Left','Up','Down','Middle','Equator','Side']
    def __init__(self):
        self.cubes=[]
        self.solving_color=''
        self.solving_face=''
        self.opposite_color=''
        self.opposite_face=''
        self.revert_list=[]
        self.move_count=-20
        for position in Rubiks.solved_position_indices:
            self.cubes.append(Cube(position, len(Rubiks.solved_position_indices[position])))
        for cube in self.cubes:
            for index in Rubiks.solved_position_indices[cube.position]:
                cube.tiles.append(Tile(index, index))
    def __str__(self):
        """Prints 9x9 grid for each face with the corresponding color letter on each 1x1 tile."""
        current_state={0:[], 1:[], 2:[], 3:[], 4:[], 5:[]}
        t=[]
        for cube in self.cubes: #current_state={orientation:[(position index, color index)...]
            if cube.type!=1:
                for tile in cube.tiles:
                    current_state[tile.orientation].append((Cube.move_face_positions[tile.orientation].index(cube.position),
                                                            tile.color))
            else:
                current_state[cube.tiles[0].orientation].append((10, cube.tiles[0].color))
        for orientation in current_state:
            f=[]
            for tup in sorted(current_state[orientation]):
                f.append(Tile.color_names[tup[1]])
            t.append("\n%s\n" % Tile.orientation_names[orientation])
            t.append("-------------\n")
            t.append("| %s | %s | %s |\n" % (f[0], f[1], f[2]))
            t.append("-------------\n")
            t.append("| %s | %s | %s |\n" % (f[7], f[8], f[3]))
            t.append("-------------\n")
            t.append("| %s | %s | %s |\n" % (f[6], f[5], f[4]))
            t.append("-------------\n")
        return ''.join(t)
    
    def scramble(self, n=20):
        """Scrambles a cube with (n)number of random moves."""
        for i in range(n):
            a=random.choice(Rubiks.move_names)
            b=random.choice(range(1,3))
            c=random.choice([True,False])
            self.move(a,b,c)


    def move(self, face, multiple=1, counter=False, revert=False):
        """Face is the string of the move needed. Ex: 'Right'
        Multiple is the number of 90degree turns.
        Counter is the bool of whether the turn is counter-clockwise."""
        if revert==True:                #move inserted into list to later be called to move back.
            self.revert_list.insert(0,(face, multiple, counter))
        if multiple==0: return
        self.move_count += 1
        if type(face)==str:
            face_index=Rubiks.move_names.index(face)
        else: face_index=face
        if counter==True: factor=-1
        else: factor=1
        position_change=2*multiple*factor
        orientation_change=1*multiple*factor
        for cube in self.cubes:                     #Data Changes Here
            if cube.position in Cube.move_face_positions[face_index]:
                current_index=Cube.move_face_positions[face_index].index(cube.position)
                cube.position=Cube.move_face_positions[face_index][index_change(current_index,position_change,8)]
                for tile in cube.tiles:
                    if tile.orientation!=face_index:
                        current_index=Cube.move_orientation[face_index].index(tile.orientation)
                        tile.orientation=Cube.move_orientation[face_index][index_change(current_index,orientation_change,4)]
    


    def edge_turn_to(self, position, o_turned, o_desired, revert=False):
        """Turns(o_turned) an edge(position) to a specific orientation(o_desired)."""
        icurr=Cube.move_face_positions[o_turned].index(position)
        idest=Cube.move_face_positions[o_turned].index(find_edge_position_intersect(o_turned, o_desired))
        m,c=shortest_distance(icurr, idest, 2)
        self.move(o_turned, m, c, revert)
    def corner_turn_to(self, position, o_turned, orientation2, orientation3, revert=False):
        """Turns(o_turned) a corner(position) to a position that intersects(o_turned, orientation2, orientation3)."""
        icurr=Cube.move_face_positions[o_turned].index(position)
        idest=Cube.move_face_positions[o_turned].index(find_corner_position_intersect(o_turned, orientation2, orientation3))
        m,c=shortest_distance(icurr, idest, 2)
        self.move(o_turned, m, c, revert)
    def orientation_turn_to(self, o_turned, o_current, o_desired, revert=False):
        """Turns(o_turned) an orientation(o_current) to another orientation(o_desired)."""
        icurr=Cube.move_orientation[o_turned].index(o_current)
        idest=Cube.move_orientation[o_turned].index(o_desired)
        m,c=shortest_distance(icurr, idest, 1)
        self.move(o_turned, m, c, revert)


    def revert(self, execution_order=False):
        """Executes the moves in the revert list, but in the opposite direction.
        Execution_order is True if the moves are to executed in the order they were received."""
        if execution_order==True:
            self.revert_list.reverse()
        for move in self.revert_list:
            f,m,c=move
            if c==True: c=False
            elif c==False: c=True
            self.move(f, m, c)
        self.revert_list=[]


    def middle_orientation_of(self, color):
        """Returns the orientation of the middle tile that corresponds to the color."""
        for cube in self.cubes:
            if cube.type==1:
                for tile in cube.tiles:
                    if tile.color==color: return tile.orientation
    def edge_tile_info(self, cube):
        """Returns data of cube for first layer edge solve."""
        for tile in cube.tiles:
            if tile.color not in [self.solving_color, self.opposite_color]:
                other_side=tile
            else: st=tile
        return st, other_side
    def edge_second_layer_tile_info(self, cube):
        """Returns data of cube for second layer edge solve."""
        for tile in cube.tiles:
            if tile.orientation==self.opposite_face:
                primary=tile
            else: tertiary=tile
        return primary, tertiary
    def corner_tile_info(self, cube):   ##Simplify##
        """Returns data of cube for first layer corner solve."""
        tile_info=[]
        t=0
        for tile in cube.tiles:
            if tile.color!=self.solving_color:
                tile_info.append(tile)
                if tile.orientation not in [self.opposite_face, self.solving_face]:
                    t +=1
            else:
                st=tile
        if t==2:
            primary_side=tile_info[0]
            tertiary_side=tile_info[1]
        elif t==1:
            for tile in tile_info:
                if tile.orientation in [self.opposite_face, self.solving_face]:
                     primary_side=tile
                else:
                     tertiary_side=tile
        return st, primary_side, tertiary_side

    
    ###############################################
    ############### Solving Functions #############
    ###############################################


    def solve_initiate(self, color):
        """After a Rubiks is scrambled, this function will define the solving parameters
        according to the color to be solved for first."""
        self.solving_color=Tile.color_names.index(color)
        self.opposite_color=Tile.color_opposites[self.solving_color]
        self.solving_face=self.middle_orientation_of(self.solving_color)
        self.opposite_face=self.middle_orientation_of(self.opposite_color)
        for cube in self.cubes:
            for tile in cube.tiles:
                tile.middle_orientation=self.middle_orientation_of(tile.color)


    def solve_edge_opposite(self, edge, st, ot):
        """Solves edge on the opposite face."""
        if st.orientation==self.opposite_face:     
            self.edge_turn_to(edge.position, self.opposite_face, ot.middle_orientation)
            self.move(ot.middle_orientation, 2)
        else:              
            self.edge_turn_to(edge.position, ot.orientation, ot.middle_orientation)
            self.move(ot.middle_orientation, 1)
            self.move(self.solving_face, 1)
            self.move(ot.orientation, 1, True)
            self.move(self.solving_face, 1 , True)
    def solve_edge_side(self, edge, st, ot):
        """Solves edge between solving face and opposite face."""
        self.edge_turn_to(find_edge_position_intersect(ot.middle_orientation, self.solving_face), self.solving_face, ot.orientation, revert=True)
        self.edge_turn_to(edge.position, ot.orientation, self.solving_face)
        self.revert()
    def solve_edge_same(self, edge, st, ot):
        """Solves edge on the solving face."""
        if is_solved([edge])==True: return
        if st.orientation==self.solving_face:
            self.move(ot.orientation, 1, revert=True)
            self.edge_turn_to(find_edge_position_intersect(ot.middle_orientation, self.solving_face), self.solving_face, ot.orientation, revert=True)
            self.revert(execution_order=True)
        else: 
            self.move(st.orientation, 1)
            self.edge_turn_to(find_edge_position_intersect(ot.middle_orientation, self.solving_face), self.solving_face, ot.orientation, revert=True)
            self.edge_turn_to(edge.position, ot.orientation, self.solving_face)
            self.revert()
    def solve_first_edges(self):
        """Solves first layer edges."""
        for i in range(4):
            for cube in self.cubes:
                if cube.type==2 and cube.solved==False:
                    for tile in cube.tiles:
                        if tile.color==self.solving_color:
                            st, ot=self.edge_tile_info(cube)
                            if cube.position in Cube.move_face_positions[self.solving_face]: self.solve_edge_same(cube, st, ot)
                            elif cube.position in Cube.move_face_positions[self.opposite_face]: self.solve_edge_opposite(cube, st, ot)
                            else: self.solve_edge_side(cube, st, ot)
                            cube.solved=True
                            break

    def solve_corner_same(self, corner):
        """Solves corner on the solving face."""
        st, primary, tertiary=self.corner_tile_info(corner)
        if st.orientation==self.solving_face:
            if primary.orientation==primary.middle_orientation: return
            self.orientation_turn_to(primary.orientation, tertiary.orientation, self.opposite_face, True)
            self.move(self.opposite_face, 1)
            self.revert()
            self.solve_corner_opposite(corner)
        else:
            self.orientation_turn_to(st.orientation, tertiary.orientation, self.opposite_face, True)
            self.move(self.opposite_face, 2)
            self.revert()
            self.solve_corner_opposite(corner)
    def solve_corner_opposite(self, corner):
        """Solves corner on the opposite face."""
        st, primary, tertiary=self.corner_tile_info(corner)
        between_mids=find_edge_position_intersect(primary.middle_orientation, tertiary.middle_orientation)
        if st.orientation==self.opposite_face:
            self.orientation_turn_to(self.opposite_face, primary.orientation, primary.middle_orientation)
            self.edge_turn_to(between_mids, tertiary.middle_orientation, self.opposite_face, True)
            self.move(self.opposite_face, 2)
            self.revert()
        self.orientation_turn_to(self.opposite_face, st.orientation, primary.middle_orientation)
        self.edge_turn_to(between_mids, primary.middle_orientation, self.opposite_face, True)
        self.orientation_turn_to(self.opposite_face, primary.orientation, primary.middle_orientation)
        self.revert()
    def solve_first_corners(self):
        """Solves first layer corners."""
        for cube in self.cubes:
            if cube.type==3 and cube.solved==False:
                for tile in cube.tiles:
                    if tile.color==self.solving_color:
                        if cube.position in Cube.move_face_positions[self.solving_face]: self.solve_corner_same(cube)
                        elif cube.position in Cube.move_face_positions[self.opposite_face]: self.solve_corner_opposite(cube)
                        cube.solved=True
                        break

    def pull_edge_out(self, edge):
        """Pulls and edge cube out of the second layer and places in third layer."""
        middle_orientations=[]
        for i in range(6):
            if edge.position in Cube.move_face_positions[i]:
                middle_orientations.append(i)
        mo1=middle_orientations[0]
        mo2=middle_orientations[1]
        self.orientation_turn_to(mo1, self.solving_face, mo2, True)
        self.orientation_turn_to(self.opposite_face, mo2, mo1)
        self.revert()
        self.orientation_turn_to(self.opposite_face, mo2, mo1, True)
        self.orientation_turn_to(mo2, self.solving_face, mo1, True)
        self.revert(True)
    def solve_edge_second_layer(self, edge):
        """Solves edge cube of second layer from third layer position."""
        primary, tertiary=self.edge_second_layer_tile_info(edge)
        opposing_primary=self.middle_orientation_of(Tile.color_opposites[primary.color])
        self.orientation_turn_to(self.opposite_face, tertiary.orientation, opposing_primary)
        self.orientation_turn_to(primary.middle_orientation, self.solving_face, tertiary.middle_orientation, True)
        self.orientation_turn_to(self.opposite_face, tertiary.orientation, tertiary.middle_orientation)
        self.revert()
        self.orientation_turn_to(self.opposite_face, tertiary.orientation, primary.middle_orientation, True)
        self.orientation_turn_to(tertiary.middle_orientation, self.solving_face, primary.middle_orientation, True)
        self.revert(True)
    def solve_second_layer(self):
        """Solves second layer."""
        edges=[]
        for cube in self.cubes:
            if cube.type==2 and is_solved([cube])==False:
                colors=[tile.color for tile in cube.tiles]
                if self.solving_color not in colors and self.opposite_color not in colors:
                    edges.append(cube)
        for cube in edges:
            if cube.position in Cube.move_face_positions[self.opposite_face]:
                self.solve_edge_second_layer(cube)
                cube.solved=True
            else:
                self.pull_edge_out(cube)
                self.solve_edge_second_layer(cube)
                cube.solved=True

    def orient_third_edge_four(self, non_oriented):
        """Orients four of the edges on the third layer."""
        orientations=[0, 1, 2, 3, 4, 5]
        orientations.remove(self.opposite_face)
        orientations.remove(self.solving_face)
        a_orientation=orientations.pop()
        a_opposite=Tile.color_opposites[a_orientation]
        orientations.remove(a_opposite)
        b_orientation=orientations.pop()
        b_opposite=orientations.pop()
        self.orientation_turn_to(a_orientation, self.opposite_face, b_orientation)
        self.orientation_turn_to(b_orientation, self.opposite_face, a_opposite)
        self.orientation_turn_to(a_opposite, self.opposite_face, b_opposite, True)
        self.move(self.opposite_face, 2)
        self.revert()
        self.orientation_turn_to(self.opposite_face, a_orientation, b_orientation)
        self.orientation_turn_to(a_opposite, b_orientation, self.opposite_face, True)
        self.orientation_turn_to(self.opposite_face, b_orientation, a_orientation)
        self.revert()
        self.orientation_turn_to(self.opposite_face, b_orientation, a_orientation)
        self.orientation_turn_to(b_orientation, a_opposite, self.opposite_face)
        self.orientation_turn_to(a_orientation, b_orientation, self.opposite_face)
        self.solve_third_edge_four_preparation(non_oriented)
    def orient_third_edge_two(self, oriented, non_oriented):
        """Orients two of the edges in the third layer."""
        for tile in non_oriented[0].tiles:
            if tile.color==self.opposite_color:
                a=tile.orientation
        for tile in non_oriented[1].tiles:
            if tile.color==self.opposite_color:
                b=tile.orientation
        directly_across=(a==Tile.color_opposites[b])
        if directly_across==True:
            orientations=[0, 1, 2, 3, 4, 5]
            for each in [self.opposite_face, self.solving_face, a, b]:
                orientations.remove(each)
            c=orientations.pop()
            self.orientation_turn_to(a, self.opposite_face, c, True)
            self.orientation_turn_to(c, a, self.opposite_face)
            self.orientation_turn_to(self.opposite_face, c, a, True)
            self.orientation_turn_to(c, self.opposite_face, a)
            self.revert()
        else:
            self.orientation_turn_to(a, self.opposite_face, b, True)
            self.orientation_turn_to(self.opposite_face, b, a)
            self.orientation_turn_to(b, a, self.opposite_face, True)
            self.orientation_turn_to(self.opposite_face, a ,b)
            self.revert()
        oriented += non_oriented
        self.solve_third_edge_four_preparation(oriented)
    def solve_third_edge_four_preparation(self, oriented):
        """Orients the third layer so that 1 of the edges is solved, unless all 4 are already solved."""
        correct=0
        while correct in [0,2]:
            correct=self.count_third_edge_four(oriented)
            if correct==0:
                self.move(self.opposite_face, 1)
            elif correct==4: return
            elif correct==2:
                self.move(self.opposite_face, 2)
                if self.count_third_edge_four(oriented)==2:
                    t=[]
                    for cube in oriented:
                        for tile in cube.tiles:
                            if tile.color!=self.opposite_color:
                                t.append(tile)
                    unmoved=t.pop()
                    for tile in t:
                        if tile.orientation==Tile.color_opposites[unmoved.orientation]:
                            unmoved_opposite=tile
                            break
                    t.remove(unmoved_opposite)
                    mover=t.pop()
                    self.orient_third_edge_mix(unmoved, mover)
        t=[]
        for cube in oriented:
            for tile in cube.tiles:
                if tile.color!=self.opposite_color:
                    t.append(tile)
        for tile in t:
            if tile.orientation==tile.middle_orientation:
                unmoved=tile
                t.remove(tile)
                break
        for i in range(6,9):
            if self.opposite_face not in Cube.move_orientation[i] and self.solving_face not in Cube.move_orientation[i]:
                indexx=Cube.move_orientation[i].index(unmoved.orientation)+1
                if indexx>3:
                    indexx -=4
                mover_middle=Cube.move_orientation[i][indexx]
                break
        for tile in t:
                if tile.orientation==Tile.color_opposites[unmoved.middle_orientation]:
                    unmoved_opposite=tile
                    t.remove(tile)
                    break
        mover=t.pop()
        mover_opposite=t.pop()
        self.solve_third_edge_four(unmoved, unmoved_opposite, mover, mover_opposite)
    def orient_third_edge_mix(self, unmoved, mover):
        """Mixes the third layer edges if 1 solved edge cannot be attained."""
        self.orientation_turn_to(mover.middle_orientation, self.solving_face, unmoved.middle_orientation, True)
        self.orientation_turn_to(self.opposite_face, mover.middle_orientation, unmoved.middle_orientation)
        self.revert()
        self.orientation_turn_to(self.opposite_face, mover.middle_orientation, unmoved.middle_orientation)
        self.orientation_turn_to(mover.middle_orientation, self.solving_face, unmoved.middle_orientation, True)
        self.move(self.opposite_face, 2)
        self.revert()
    def solve_third_edge_four(self, unmoved, unmoved_opposite, mover, mover_opposite):
        """Solves the edges on the third layer after they have been oriented."""
        self.orientation_turn_to(mover.orientation, self.solving_face, unmoved.middle_orientation, True)
        self.orientation_turn_to(self.opposite_face, mover.middle_orientation, mover.orientation)
        self.revert()
        self.orientation_turn_to(self.opposite_face, mover_opposite.orientation, mover_opposite.middle_orientation)
        self.orientation_turn_to(mover_opposite.orientation, self.solving_face, unmoved.middle_orientation, True)
        self.orientation_turn_to(self.opposite_face, unmoved.orientation, unmoved.middle_orientation)
        self.revert()
    def count_third_edge_four(self, cubes):
        """Counts the number of solved cubes.
        Cubes is a list of cubes."""
        count=0
        for cube in cubes:
            for tile in cube.tiles:
                if tile.color!=self.opposite_color and tile.orientation==tile.middle_orientation:
                    count += 1
                    break
        return count
    def solve_third_edges(self):
        """Solves the third layer of edges."""
        non_oriented=[]
        oriented=[]
        for cube in self.cubes:
            if cube.type==2 and cube.solved==False:
                for tile in cube.tiles:
                    if tile.color==self.opposite_color:
                        if tile.orientation==self.opposite_face:
                            oriented.append(cube)
                        else:
                            non_oriented.append(cube)
        if len(oriented)==0: self.orient_third_edge_four(non_oriented)
        elif len(oriented)==2: self.orient_third_edge_two(oriented, non_oriented)
        elif len(oriented)==4: self.solve_third_edge_four_preparation(oriented)
        oriented += non_oriented
        for cube in oriented:
            cube.solved=True

    def algorithm_third_corner_orient(self, a, b, direction):
        """Algorithm for orienting third layer corners.
        a=orientation
        b=orientation perpendicular to a.
        Direction=bool"""
        c=self.solving_face
        if direction==True:
            self.orientation_turn_to(b, a, c, True)
            self.orientation_turn_to(c, a , b, True)
            self.revert(True)
            self.orientation_turn_to(b, a, c, True)
            self.orientation_turn_to(c, a, b)
            self.revert()
        elif direction==False:
            self.orientation_turn_to(b, a, c, True)
            self.orientation_turn_to(c, b , a, True)
            self.revert(True)
            self.orientation_turn_to(b, a, c, True)
            self.orientation_turn_to(c, b, a)
            self.revert()
    def orient_third_corners(self, non_oriented):
        """Orients third layer corners."""
        length=len(non_oriented)
        if length==4:
            solving_position=non_oriented[0].position
            for tile in non_oriented[0].tiles:
                    if tile.color==self.opposite_color:
                        a=tile.orientation
                    elif tile.orientation!=self.opposite_face:
                        b=tile.orientation
            for i in range(4):
                for cube in self.cubes:
                    if cube.position==solving_position:
                        for tile in cube.tiles:
                            if tile.orientation==a:
                                flag=tile.color==self.opposite_color
                                break
                        break
                self.algorithm_third_corner_orient(a, b, flag)
                self.move(self.opposite_face, 1)
        elif length==3:
            t=[]
            for tile in non_oriented[0].tiles:
                if tile.color==self.opposite_color:
                    d=tile.orientation
                    break
            for cube in non_oriented[1:]:
                for tile in cube.tiles:
                    if tile.color==self.opposite_color:
                        a=tile.orientation
                    elif tile.orientation!=self.opposite_face:
                        b=tile.orientation
                t.append((a, b))
            for a,b in t:
                self.algorithm_third_corner_orient(a, b, True)
                self.orientation_turn_to(self.opposite_face, d, a)
                self.algorithm_third_corner_orient(a, b, False)
                self.orientation_turn_to(self.opposite_face, a, d)
        elif length==2:
            for tile in non_oriented[0].tiles:
                if tile.color==self.opposite_color:
                    d=tile.orientation
                    break
            for tile in non_oriented[1].tiles:
                if tile.color==self.opposite_color:
                    a=tile.orientation
                elif tile.orientation!=self.opposite_face:
                    b=tile.orientation
            self.algorithm_third_corner_orient(a, b, True)
            self.orientation_turn_to(self.opposite_face, d, b)
            self.algorithm_third_corner_orient(a, b, False)
            self.orientation_turn_to(self.opposite_face, b, d)
    def algorithm_third_corner_solve(self, solving_order):
        """Algorithm for solving third layer corners."""
        t=[tile.orientation for tile in solving_order[0].tiles if tile.orientation!=self.opposite_face]
        a,b=t
        c=self.solving_face
        static_position=solving_order[0].position
        self.orientation_turn_to(a, b, c)
        self.orientation_turn_to(c, b, a)
        self.orientation_turn_to(a, c, b)
        for cube in self.cubes:
            if cube.position==static_position:
                substitute_cube=cube
                break
        self.corner_turn_to(solving_order[1].position, self.opposite_face, a, b)
        self.orientation_turn_to(a, b, c)
        self.orientation_turn_to(c, a, b)
        self.orientation_turn_to(a, c, b)
        self.corner_turn_to(solving_order[2].position, self.opposite_face, a, b)
        self.orientation_turn_to(a, b, c)
        self.orientation_turn_to(c, b, a)
        self.orientation_turn_to(a, c, b)
        self.corner_turn_to(substitute_cube.position, self.opposite_face, a, b)
        self.orientation_turn_to(a, b, c)
        self.orientation_turn_to(c, a, b)
        self.orientation_turn_to(a, c, b)

    def solve_third_corners(self):
        """Solves third layer corners."""
        non_oriented=[]
        for cube in self.cubes:
            if cube.type==3 and cube.solved==False:
                for tile in cube.tiles:
                    if tile.color==self.opposite_color:
                        if tile.orientation!=self.opposite_face:
                            non_oriented.append(cube)
                        break
        self.orient_third_corners(non_oriented)
        for i in range(2):
            not_solved=[]
            for cube in self.cubes:
                for tile in cube.tiles:
                    if tile.orientation!=tile.middle_orientation:
                        not_solved.append(cube)
                        break
            if len(not_solved)==0:
                break
            solving_order=[]
            colors=[]
            first=not_solved.pop()
            solving_order.append(first)
            for tile in first.tiles:
                colors.append(self.middle_orientation_of(tile.color))
            colors.sort()
            for cube in not_solved:
                test=[]
                for tile in cube.tiles:
                    test.append(tile.orientation)
                test.sort()
                if test==colors:
                    solving_order.append(cube)
                    not_solved.remove(cube)
                    break
            solving_order.append(not_solved.pop())
            self.algorithm_third_corner_solve(solving_order)
            if len(not_solved)==0:
                break

    def solve_cube(self, solving_side):
            self.scramble(20)
            self.solve_initiate(solving_side)
            self.solve_first_edges()
            self.solve_first_corners()
            self.solve_second_layer()
            self.solve_third_edges()
            self.solve_third_corners()

    def solved_check(self):
        correct=0
        for cube in self.cubes:
            for tile in cube.tiles:
                if tile.orientation==tile.middle_orientation:
                    correct +=1
            cube.solved=False
        return correct==54

if __name__ == "__main__":
        cube = Rubiks()
        for i in range (10):
            cube.scramble(20)
            cube.solve_cube("O")
            print cube.solved_check()