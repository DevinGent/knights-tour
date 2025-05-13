import pandas as pd

# This script determines a solution to the game Knight's Tour via exhaustion. As a non-optimal method this script performs
# noticeably worse when the number of rows and columns of the grid are increased. 

# Tracking the total moves checked in finding a solution.
TOTAL_MOVES_CHECKED=0

class LegalMoves:
    """A class which contains a method to determine the available moves (i.e. not off the board) for a game of Knight's Tour)."""

    # From any given position on the board a knight can move two spaces in one direction and then turn and move one more.
    # This list of offsets represents the directions a knight can travel.
    OFFSETS=[
        (2,1),
        (2,-1),
        (1,-2),
        (-1,-2),
        (-2,1),
        (-2,-1),
        (1,2),
        (-1,2)
    ]

    def __init__(self, rows,columns):
        self.min_x=0
        self.max_x=rows-1
        self.min_y=0
        self.max_y=columns-1

    def get_legal_moves(self, coordinates: tuple):
        """Takes a pair of starting coordinates and determines what moves the knight can make (if the knight is allowed to reuse spaces).
        Returns a list of tuples representing coordinates."""

        available_moves=[]
        (x,y)=coordinates
        for (i,j) in self.OFFSETS:
            if self.min_x<=x+i<=self.max_x and self.min_y<=y+j<=self.max_y:
                available_moves.append((x+i,y+j))
        # After completing this loop we return the acquired list.
        return available_moves

def display_grid(rows=2,columns=3):
    """Prints a sample grid to make it easier to demonstrate how space numbers works."""

    print(f"The following is a {rows}x{columns} ({rows} rows, {columns} columns) grid of spaces.")
    print("We number them from left to right and top to bottom as follows:")
    for i in range(1,rows*columns+1):
        print(i,end='\t')
        if i % columns==0:
            print()


def find_tour(rows:int,columns:int,starting_space=None,visited_spaces=None):
    """Accepts the number of rows and columns in a grid and optionally a starting space (by default the top left space),
    then works to determine a tour that covers all the spaces without reusing any space. If a tour is found 
    the function returns a list of coordinates representing the sequence of moves used to complete the tour.
    
    The optional argument visited_spaces allows the user to provide a list of spaces which have previously been visited. In
    this case the user must ensure that those spaces could be legitimately achieved using a knight's moves and must include
    the argument starting_space to represent the knight's current position."""

    # If no starting space is given.
    if starting_space==None:
        # We default to the first space.
        if visited_spaces==None:
            starting_space=1
        # We raise an error if no starting space is given but the grid has already been partially traveled.
        else:
            raise ValueError("If visited_spaces have been provided you must also provide the knight's current position as the argument starting_space")


    # Checking that rows and columns are valid integers.
    if rows<3 or columns<3:
        raise ValueError("There must be at least three rows and three columns.")


    # We build a dataframe to track moves.
    grid=[]
    for i in range(rows):
        for j in range(columns):
            grid.append((i,j))

    # We include columns for the coordinate of each space along with it's label (starting at 1).
    df=pd.DataFrame({'Coordinates':grid})
    df['Space']=df.index+1
    # The dataframe will be indexed by the coordinates.
    df.set_index('Coordinates', inplace=True)
    # We include a column to track which spaces have been visited and in what order.
    df['Move-Number']=None




    # We locate the starting coordinates.
    if starting_space in list(df['Space']):
        starting_coordinates=df[df['Space']==starting_space].index[0]
    else:
        raise ValueError(f"The starting space must be an integer in the range from 1 to {rows*columns}.")

    # If no visited spaces are included we have the following spaces left to visit.
    remaining_spaces=rows*columns-1

    # If visited spaces have been included we add them as if they've been visited.
    if visited_spaces!=None:
        # If every space is legal.
        if set(visited_spaces).issubset(df['Space']):
            # We set all the moves to 0 for the spaces which have been visited.
            df.loc[df['Space'].isin(visited_spaces),'Move-Number']=0
            # Calculating how many spaces are still empty.
            remaining_spaces=rows*columns-len(set(visited_spaces+[starting_space]))
        # If even one space is illegal.
        else:
            raise ValueError(f"All visited spaces must be integers in the range from 1 to {rows*columns}.")
        
    # We create a move validator to match the given rows and columns.
    move_validator=LegalMoves(rows,columns)
    # We set the move number of the starting space.
    df.at[starting_coordinates,'Move-Number']=1


    # The result will be a dataframe column of moves.
    result=drill(df,starting_coordinates,move_validator,1,remaining_spaces)
    if result.empty==True:
        print("The program was unable to determine a tour.")
    # If a tour was found we replace the move number column, sort in the order the moves were made, and return the result as a dataframe.
    df['Move-Number']=result
    df.sort_values(by=['Move-Number'], inplace=True)
    return df



def drill(dataframe,current_coordinate,move_validator,moves_made,remaining_spaces):
    """Tries to select another move to add to the current list of moves. If successful returns a column representing the
    order of moves, if unsuccessful returns an empty Series."""

    # Each time we drill we increment the counter of total moves checked.
    global TOTAL_MOVES_CHECKED
    TOTAL_MOVES_CHECKED+=1

    if remaining_spaces==0:
        return dataframe['Move-Number']
    else:
        for space in move_validator.get_legal_moves(current_coordinate):
            if dataframe.at[space,'Move-Number']==None:
                new_moves=moves_made+1
                new_df=dataframe.copy()
                new_df.at[space,'Move-Number']=new_moves
                result=drill(new_df,space,move_validator,new_moves,remaining_spaces-1)
                
                if result.empty == False:
                    return result
    return pd.Series()
                

def main():

    # Tracking the time it takes to solve the puzzle.
    import time
    start=time.time()

    # Provide the number of rows and columns here.
    rows=5
    columns=5

    # Provide the starting space (or if spaces have been visited the one that the knight is currently on).
    start_space=17

    # Provide a list of the spaces which have been visited (leave empty if none).
    visited_spaces=[]

    ####################
    # Leave the following settings alone.

    # Displaying a sample grid to keep track of numbering.
    display_grid(rows,columns)
    # Determining a solution if possible.
    tour=find_tour(rows,columns,start_space,visited_spaces)
    print(tour)
    
    end=time.time()
    global TOTAL_MOVES_CHECKED
    print(f"It took {end-start} seconds to solve (or fail to solve) the given tour.")
    print(f"A total of {TOTAL_MOVES_CHECKED} moves were checked in arriving at a solution.")


    

if __name__ == "__main__":

    main()



