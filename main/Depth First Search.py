import copy
import webbrowser
import timeit
colored = {}
backtracking = 0
singleton = 0
dfs_with_heuristic = 0
def check_valid(graph):
    "Check the graph is valid i.e States are linked properly to each other"
    for node,nexts in graph.items():
        assert(node not in nexts) # # no node linked to itself
        for next in nexts:
            assert(next in graph and node in graph[next]) # A linked to B implies B linked to A
#DFS

def get_neighbours(state,country,country_colors):
    ""
    if dfs_with_heuristic == 0:
        return country[state]
    else:
        if singleton == 0:
            candts_with_add_info = [
                (
                -len({colored[neigh] for neigh in country[n] if neigh in colored}),#Minimum Remaining Value Hueristic
                -len({neigh for neigh in country[n] if neigh not in colored}),# Degree Heuristic
                n
                ) for n in country[state] if n not in colored]
            #Get Neighbours based on heuristic value
        else:
            candts_with_add_info = [
                (
                # For singleton Sort the neighbours based on their Colors Remaining
                -100 if (len(country_colors[n]) == 1) else 100,
                -len({colored[neigh] for neigh in country[n] if neigh     in colored}), #Minimum Remaining Value Hueristic
                -len({neigh          for neigh in country[n] if neigh not in colored}), # Degree Heuristic
                #then calculate the number of neighbours)
                n
            #"Neigbours"
            ) for n in country[state] if n not in colored]
        candts_with_add_info.sort()
        print(candts_with_add_info, "--Sort - ()()()()()")
        # Return Neighbours in an ordered way with given - heurisitc
        if singleton == 0:
            canddts= [n for _,_,n in candts_with_add_info]
        else:
            canddts = [n for _,_,_,n in candts_with_add_info]
        return canddts

def get_colors(state,country,country_colors):
    # Get Colours
    if dfs_with_heuristic == 0:
        return country_colors[state]
    else:
        # Get Colors based on Least Constraining Value
        a = []
        for color in country_colors[state]:
            no_of_colors = 0
            a.append([color])
            for neigh in country[state]:
                if color in country_colors[neigh]:
                    no_of_colors = no_of_colors + len(country_colors[neigh]) - 1
                else:
                    no_of_colors = no_of_colors + len(country_colors[neigh])
            a[a.index([color])].append(no_of_colors)
        a = sorted(a,key = lambda x:x[1],reverse = True)
        a = [x[0] for x in a]
        return a

# Solve DFS
def solve_problem_DFS(state,country,country_colors):
    increment_color = 0
    flag = 0
    global backtracking
    # Loop on all the colors value
    for color in get_colors(state,country,country_colors):
        for neigh in country[state]:
            if neigh in colored and colored[neigh] == color:
                increment_color = 1
                break
        if increment_color == 1:
            increment_color = 0
            continue
        colored[state] = color
        print("Trying to give color %s to %s" %(colored[state],state))
        # Calling the neighbour Value using DFS
        for neigh in get_neighbours(state,country,country_colors):
            if neigh not in colored:
                #DFS : - if no values found for child - pop the value and check for another value
                if (solve_problem_DFS(neigh, country, country_colors) == False):
                    colored.pop(state)
                    flag = 1
                    break
        if flag == 0:
            print("Gave color %s to %s" % (colored[state],state))
            return True
        else:
            flag = 0
            continue
    # If none of the values work then backtrack
    print("No Value for state%s: - Backtracking "%(state))
    backtracking = backtracking + 1
    return False

#DFS with Forward Chaining
# Remove Colors from neighbours
def reduce_domain(state,country,cntry_colors):
    for j in country[state]:
        if colored[state] in cntry_colors[j]:
            cntry_colors[j].remove(colored[state])
            # print("Removed Color ")

# check if with the given color no neighbour will have empty domain
def reduce_domain_forward_check(color,state,country,cntry_colors):
    p = copy.deepcopy(cntry_colors)
    for j in country[state]:
        if color in p[j] :
            p[j].remove(color)
        if not check_domain(j,p):
            return False
    return True

# Check Color remaining for a given state is not empty
def check_domain(state,cntry_colors):
    if not (cntry_colors[state]) :
        return False
    return True

# DFS with Forward Chaining and singleton
def solve_problem_DFS_FC(state,country,country_colors):
    flag = 0
    increment_color = 0
    b = copy.deepcopy(country_colors)
    global backtracking
    # Loop on all the colors value
    for color in get_colors(state,country,country_colors):
        # Taking Colours of Country into temporary Variable since it will be used for backtracking
        a = copy.deepcopy(b)
        for neigh in country[state]:
            if neigh in colored and colored[neigh] == color:
                country_colors[neigh] = b[neigh] = a[neigh] = [color]
                increment_color = 1
                break
        if increment_color == 1:
            increment_color = 0
            continue
        colored[state] = color
        print("Trying to give color %s to %s" %(color,state))
        reduce_domain(state, country, a)
        print("Colors of all state after reducing their domain\n",a)
        a[state] = [color]
        if singleton == 1 and dfs_with_heuristic == 0:
            print("Neighbours of country(Singleton) %s - %s"%(state,country[state]))
            country[state] = sorted(country[state],key = lambda x:len(country_colors[x]),reverse = False)
            print(" After Sorting - Neighbours of country(Singleton) %s - %s"%(state,country[state]))
        # Calling the neighbour Value using DFS
        for neigh in get_neighbours(state,country,a):
            if neigh not in colored:
                #DFS : - if no values found for child - pop the value and check for another value
                if (solve_problem_DFS_FC(neigh,country,a)) == False :
                    colored.pop(state)
                    flag = 1
                    print("Cannot give color to",state)
                    break
        if flag == 0:
            print("Gave color %s to %s" % (colored[state], state))
            return True
        else:
            # Check for another Value if Child values not found for current one
            flag = 0
            continue
    print("No Value for state%s: - Backtracking "%(state))
    # If none of the values work then backtrack
    backtracking = backtracking + 1
    return False

AUWA  = 'AU-WA'
AUNT  = 'AU-NT'
AUSA  = 'AU-SA'
AUQ   = 'AU-QLD'
AUNSW = 'AU-NSW'
AUV   = 'AU-VIC'
AUT   = 'AU-TAS'

australia = { 
    AUT:   {AUV},
    AUWA:  {AUNT, AUSA},
    AUNT:  {AUWA, AUQ, AUSA},
    AUSA:  {AUWA, AUNT, AUQ, AUNSW, AUV},
    AUQ:   {AUNT, AUSA, AUNSW},
    AUNSW: {AUQ, AUSA, AUV},
    AUV:   {AUSA, AUNSW, AUT} 
}

au_colors= { 
    AUT:  ['red','green','blue'],
    AUWA: ['red','green','blue'],
    AUNT: ['red','green','blue'],
    AUSA: ['red','green','blue'],
    AUQ:  ['red','green','blue'],
    AUNSW:['red','green','blue'],
    AUV:  ['red','green','blue']
}

AL = "US-AL"
AK = "US-AK"
AZ = "US-AZ"
AR = "US-AR"
CA = "US-CA"
CO = "US-CO"
CT = "US-CT"
DE = "US-DE"
FL = "US-FL"
GA = "US-GA"
HI = "US-HI"
ID = "US-ID"
IL = "US-IL"
IN = "US-IN"
IA = "US-IA"
KS = "US-KS"
KY = "US-KY"
LA = "US-LA"
ME = "US-ME"
MD = "US-MD"
MA = "US-MA"
MI = "US-MI"
MN = "US-MN"
MS = "US-MS"
MO = "US-MO"
MT = "US-MT"
NE = "US-NE"
NV = "US-NV"
NH = "US-NH"
NJ = "US-NJ"
NM = "US-NM"
NY = "US-NY"
NC = "US-NC"
ND = "US-ND"
OH = "US-OH"
OK = "US-OK"
OR = "US-OR"
PA = "US-PA"
RI = "US-RI"
SC = "US-SC"
SD = "US-SD"
TN = "US-TN"
TX = "US-TX"
UT = "US-UT"
VT = "US-VT"
VA = "US-VA"
WA = "US-WA"
WV = "US-WV"
WI = "US-WI"
WY = "US-WY"

united_states_of_america = {
    AL: {GA, FL, TN, MS},
    AK: {WA},
    AZ: {CA, NV, UT, CO, NM},
    AR: {MO, OK, TX, LA, TN, MS },
    CA: {OR, NV, AZ,HI},
    CO: {WY, NE, KS, OK, NM, AZ, UT},
    CT: {NY,RI,MA},
    DE: {MD,PA,NJ},
    FL: {AL, GA},
    GA: {SC, NC, TN, AL, FL},
    HI: {CA},
    ID: {WA, MT, OR, WY, UT, NV},
    IL: {WI, IA, MO, KY, IN, MI},
    IN: {MI, IL, KY, OH},
    IA: {MN, SD, NE, MO, WI, IL},
    KS: {NE, CO, OK, MO},
    KY: {IN, IL, MO, TN, OH, WV, VA},
    LA: {AR, TX, MS},
    ME: {NH},
    MD: {PA,WV,VA,DE},
    MA: {NY,VT,NH,CT,RI},
    MI: {IL, WI, IN, OH},
    MN: {ND, SD, IA, WI},
    MS: {TN, AR, LA, AL},
    MO: {IA, NE, KS, OK, AR, IL, KY, TN},
    MT: {ID, WY, SD, ND},
    NE: {SD, CO, WY, KS, MO, IA},
    NV: {OR, ID, UT, AZ, CA},
    NH: {ME,VT,MA},
    NJ: {NY,PA,DE},
    NM: {AZ, UT, CO, OK, TX},
    NY: {PA,NJ,CT,MA,VT},
    NC: {GA, TN, SC, VA},
    ND: {MT, SD, MN},
    OH: {MI, IN, KY, WV,PA},
    OK: {KS, CO, NM, TX, AR, MO},
    OR: {WA, ID, NV, CA},
    PA: {OH,WV,DE,NJ,NY,MD},
    RI: {CT,MA},
    SC: {GA, NC},
    SD: {ND, MT, WY, NE, MN, IA},
    TN: {KY,AR, MS, MO, AL, GA, NC,VA},
    TX: {OK, NM, AR, LA},
    UT: {ID, NV, WY, CO, AZ, NM},
    VT: {MA,NY,NH},
    VA: {WV, KY, NC,TN,MD},
    WA: {OR,ID,AK},
    WV: {OH, VA, KY,PA,MD},
    WI: {MN, IL, MI, IA},
    WY: {MT, SD,NE, CO, UT, ID},
}

us_colors = {
    AL: ['red', 'green', 'blue', 'yellow'],
    AK: ['red', 'green', 'blue', 'yellow'],
    AZ: ['red', 'green', 'blue', 'yellow'],
    AR: ['red', 'green', 'blue', 'yellow'],
    CA: ['red', 'green', 'blue', 'yellow'],
    CO: ['red', 'green', 'blue', 'yellow'],
    CT: ['red', 'green', 'blue', 'yellow'],
    DE: ['red', 'green', 'blue', 'yellow'],
    FL: ['red', 'green', 'blue', 'yellow'],
    GA: ['red', 'green', 'blue', 'yellow'],
    HI: ['red', 'green', 'blue', 'yellow'],
    ID: ['red', 'green', 'blue', 'yellow'],
    IL: ['red', 'green', 'blue', 'yellow'],
    IN: ['red', 'green', 'blue', 'yellow'],
    IA: ['red', 'green', 'blue', 'yellow'],
    KS: ['red', 'green', 'blue', 'yellow'],
    KY: ['red', 'green', 'blue', 'yellow'],
    LA: ['red', 'green', 'blue', 'yellow'],
    ME: ['red', 'green', 'blue', 'yellow'],
    MD: ['red', 'green', 'blue', 'yellow'],
    MA: ['red', 'green', 'blue', 'yellow'],
    MI: ['red', 'green', 'blue', 'yellow'],
    MN: ['red', 'green', 'blue', 'yellow'],
    MS: ['red', 'green', 'blue', 'yellow'],
    MO: ['red', 'green', 'blue', 'yellow'],
    MT: ['red', 'green', 'blue', 'yellow'],
    NE: ['red', 'green', 'blue', 'yellow'],
    NV: ['red', 'green', 'blue', 'yellow'],
    NH: ['red', 'green', 'blue', 'yellow'],
    NJ: ['red', 'green', 'blue', 'yellow'],
    NM: ['red', 'green', 'blue', 'yellow'],
    NY: ['red', 'green', 'blue', 'yellow'],
    NC: ['red', 'green', 'blue', 'yellow'],
    ND: ['red', 'green', 'blue', 'yellow'],
    OH: ['red', 'green', 'blue', 'yellow'],
    OK: ['red', 'green', 'blue', 'yellow'],
    OR: ['red', 'green', 'blue', 'yellow'],
    PA: ['red', 'green', 'blue', 'yellow'],
    RI: ['red', 'green', 'blue', 'yellow'],
    SC: ['red', 'green', 'blue', 'yellow'],
    SD: ['red', 'green', 'blue', 'yellow'],
    TN: ['red', 'green', 'blue', 'yellow'],
    TX: ['red', 'green', 'blue', 'yellow'],
    UT: ['red', 'green', 'blue', 'yellow'],
    VA: ['red', 'green', 'blue', 'yellow'],
    VT: ['red', 'green', 'blue', 'yellow'],
    WA: ['red', 'green', 'blue', 'yellow'],
    WV: ['red', 'green', 'blue', 'yellow'],
    WI: ['red', 'green', 'blue', 'yellow'],
    WY: ['red', 'green', 'blue', 'yellow'],
}

# Can't be bothered to complete the East part of the map - removing unused nodes (keeping them is also a good way to test your algorithm and see if still works)
united_states_of_america = {n:neigh for n,neigh in united_states_of_america.items() if neigh}

def makeBrowser(cname):
    global colored
    
    f = open('worldmap.html','w')

    message = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>IS Project 3 - Abhishek Fulzele & Rahul Patel</title>
    <link rel="stylesheet" media="all" href="./jquery-jvectormap.css"/>
    <script src="assets/jquery-1.8.2.js"></script>
    <script src="./jquery-jvectormap.js"></script>
    <script src="../lib/jquery-mousewheel.js"></script>

    <script src="../src/jvectormap.js"></script>

    <script src="../src/abstract-element.js"></script>
    <script src="../src/abstract-canvas-element.js"></script>
    <script src="../src/abstract-shape-element.js"></script>

    <script src="../src/svg-element.js"></script>
    <script src="../src/svg-group-element.js"></script>
    <script src="../src/svg-canvas-element.js"></script>
    <script src="../src/svg-shape-element.js"></script>
    <script src="../src/svg-path-element.js"></script>
    <script src="../src/svg-circle-element.js"></script>
    <script src="../src/svg-image-element.js"></script>
    <script src="../src/svg-text-element.js"></script>

    <script src="../src/vml-element.js"></script>
    <script src="../src/vml-group-element.js"></script>
    <script src="../src/vml-canvas-element.js"></script>
    <script src="../src/vml-shape-element.js"></script>
    <script src="../src/vml-path-element.js"></script>
    <script src="../src/vml-circle-element.js"></script>
    <script src="../src/vml-image-element.js"></script>

    <script src="../src/map-object.js"></script>
    <script src="../src/region.js"></script>
    <script src="../src/marker.js"></script>

    <script src="../src/vector-canvas.js"></script>
    <script src="../src/simple-scale.js"></script>
    <script src="../src/ordinal-scale.js"></script>
    <script src="../src/numeric-scale.js"></script>
    <script src="../src/color-scale.js"></script>
    <script src="../src/legend.js"></script>
    <script src="../src/data-series.js"></script>
    <script src="../src/proj.js"></script>
    <script src="../src/map.js"></script>

    <script src="assets/jquery-jvectormap-world-mill-en.js"></script>
    <script src="assets/jquery-jvectormap-us-aea-en.js"></script>
    <script src="assets/jquery-jvectormap-aus-en.js"></script>

    <script>
        jQuery.noConflict();
        jQuery(function(){
            var $ = jQuery;
            
            $('#map1').vectorMap({
                map: '"""
    message1 = """',
                panOnDrag: true,       
                series: {                    
                    regions: [{
                        scale: {
                            red: '#ff0000',
                            green: '#00ff00',
                            blue: '#0000ff',
                            yellow: '#ffee34'
                        },
                        attribute: 'fill',
                        values: 
    """
    message2 = """
                        ,
                        legend: {
                            horizontal: true,
                            title: 'Color'
                        }
                    }]
                }
            });
        })
    </script>
    </head>
    <body>
        <div id="map1" style="width: 600px; height: 400px"></div>
    </body>
    </html>
    """

    x = str(cname)

    mainmessage = message + x + message1 + str(colored) + message2

    f.write(mainmessage)
    f.close()

    webbrowser.open_new_tab('worldmap.html')


if __name__ ==  '__main__':

    print("1. America      2. Australia")
    country_name = int(input("Which country would you like to select:\n "))

    cname = ""
    fullname = {}
    color = {}
    abbr = ""

    if country_name == 1:
        cname = "us_aea_en"
        fullname = united_states_of_america
        color = us_colors
        abbr = WV
    elif country_name == 2:
        cname = "au_mill"
        fullname = australia
        color = au_colors
        abbr = AUWA
    else:
        print("Enter a proper value")
        exit(0)
    check_valid(united_states_of_america)
    print("----------------------\n1. DFS\n2. DFS with Forward Checking\n3. DFS with Forward Checking and Singleton\n4. DFS With Heuristic\n5. DFS with Heuristic and Forward Checking\n6. DFS with heuristic, Forward Checking and singleton\n----------------------")
    algo_name = int(input("Which algorithm would you like to select:\n"))

    start = timeit.default_timer()

    print("Starting with State",abbr)

    if algo_name == 1:
        if (solve_problem_DFS(abbr, fullname, color)):
            print(colored)
    elif algo_name == 2:
        if (solve_problem_DFS_FC(abbr, fullname, color)):
            print("Count",len(colored.keys()))
            print(colored)
    elif algo_name == 3:
        singleton = 1
        if solve_problem_DFS_FC(abbr, fullname, color):
            print("Count",len(colored.keys()))
            print(colored)
    elif algo_name == 4:
        dfs_with_heuristic = 1
        if (solve_problem_DFS(abbr, fullname, color)):
            print(colored)
    elif algo_name == 5:
        dfs_with_heuristic = 1
        if (solve_problem_DFS_FC(abbr, fullname, color)):
            print(colored)
    elif algo_name == 6:
        dfs_with_heuristic = 1
        singleton = 1
        if (solve_problem_DFS_FC(abbr, fullname, color)):
            print(colored)
    else:
        print("Enter a proper value")
        exit(0)
    stop = timeit.default_timer()
    print('\nTime: ', stop - start)
    print("Number of Backtracking:-",backtracking)
    makeBrowser(cname)
    colored.clear()
