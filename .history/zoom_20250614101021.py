zoom_levels = {
    (0 , 50) :    19, 
    (50, 100) :   18,
    (101, 200) :  17,
    (201, 500) :  16,
    (501, 999) :  16,
    (1000, 1500): 15,
    (1501, 4500): 14,
    (4501, 12500): 13,
    (12501, 30000):12,
    (30001, 45000):11,
    (45001, 60000):10,
    (60001, 100000):9,
    (100001,170000):8,
    (170001,400000):7,
    (400001,700000):6,
    (700001,1500000):5,
    (1500001,2500000):4,
    (2500001, float('inf')):3    
}

#Funcion que determina el zoom para TkinterMapView
def get_zoom_level(radio):
            for (min_radio, max_radio), zoom in zoom_levels.items():
                if min_radio <= radio <= max_radio:
                    return zoom