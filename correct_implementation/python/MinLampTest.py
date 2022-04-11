# Declare: the question and the min_lamp_solution function are designed and 
#  written by professor Ting Hu from Queen's University. 

from hypothesis import given, settings, example, Phase, strategies as st
import unittest 
import time
import matplotlib.pyplot as plt
import numpy as np
import pickle

class min_lamp:

    def min_lamp_solution(r): 
        
        n = len(r)-1 # the goal is to illuminate the inteverl [0,n]
        lamps = [] # a list of tuples
        lamps_to_add = [] # a list of indices of lamps that should be turned on
        
        # each lamp is represented as a tuple of (left_endpoint, right_endpoint, original_index_before_sorting)
        for i in range(n+1):
            lamps.append((max(0,i-r[i]),i+r[i],i)) 
        
        lamps.sort(key=lambda tup:tup[0]) # sort the lamps by their left endpoints
        
        if lamps[0][0] > 0: # position 0 cannot be covered by any lamp
            return None

        # find the first lamp to add to the "on" list
        k = 1
        first_lamp = 0
        current_right = lamps[0][1]
        while k <= n and lamps[k][0] == 0: # search all lamps with the left endpoint = 0
            if lamps[k][1]>current_right:
                current_right = lamps[k][1]
                first_lamp = k
            k = k+1
        lamps_to_add.append(lamps[first_lamp][2]) # turn on the first lamp with the furthest right endpoint

        # add the subsequent lamps
        # the key to maintaining a O(n) complexity is avoiding going back to lamps already been searched
        i = k # continue the search with lamp k  
        # check one lamp at a time, stop when all the lamps are checked or position n is illuminated
        while i <= n and current_right < n: 
            if current_right < lamps[i][0]: # the area between current_right and the next lamp's left endpoint cannot be covered
                return None
            else: # find the first next lamp that overlaps with current_right and has the furtherest right endpoint
                next_lamp = i
                max_right = current_right
                while i <= n and lamps[i][0] <= current_right:
                    if lamps[i][1] > max_right:
                        max_right = lamps[i][1]
                        next_lamp = i
                    i = i+1
                current_right = max_right # once the next lamp is found, update current_right
                lamps_to_add.append(lamps[next_lamp][2]) # add the lamp to the "on" list using its original index
        
        return lamps_to_add
        
    def incorrect_min_lamp(r):

        n = len(r) - 1 # length aka street section 
        
        # Create the illumination list where each lamp can cover
        radiusList = []
        for i in range(0, len(r)): # O(n)
            if r[i] == 0:
                continue # do nothing lamp is broken

            elif (i-r[i] <= 0) and (i+r[i] >= n):
                return [i+1] # one lamp covers the entire street 
            
            else:
                radiusList.append((i-r[i], i+r[i])) # start, end

        if len(radiusList)==0: # every lamps is broken 
            return None # no solution 
        
        # sort using the start (i - r[i]) 
        radiusList.sort() # O(nlogn)
        
        # print(radiusList) 

        startPosition = 0 # start of the street section (city hall)
        
        turnUpList = [] # set of indices of lamp posts that can be turned
                        # on to illuminate the entire street section 
        j = 0 # goes through every lamp from index 0 to n-1

        # looks like a infinite loop but because something inside this loop will
        # eventually be returned, this does not go infinitely
        while True: # Greedy implementation down below takes O(n)

            # record illumination that covers the most roads 
            illumination = False 

            # goes through elements in radiusList that start before the
            #  startPosition. For example, at the beginning, startPosition will
            #  be 0 so any negative or 0 starting element will be considered. 
            while (j < len(radiusList)) and (startPosition >= radiusList[j][0]):

                # illumination that has the max ending point is selected
                if (type(illumination)==bool) or (radiusList[j][1] > illumination[1]):
                    
                    illumination = radiusList[j]
                    
                j+=1 # runs through the list 

            # no available illumination is found then it means
            #  illumination is not continuous 
            if type(illumination)==bool:
                return None # no solution 

            # calculate illumination's corresponding lamp position (index)
            index = illumination[0] + (illumination[1] - illumination[0]) // 2 
            turnUpList.append(index) # record it

            # find the next illumination/lamp that covers the street continuously 
            startPosition = illumination[1]

            # found illumination cover to the
            #  end of the street (intersection of Ontario and Earl)
            if n <= illumination[1]:
                return turnUpList # return solution 

class Tests(unittest.TestCase):

    @given(st.lists(
        st.integers(min_value=0, max_value=5), 
        min_size=2, max_size=None, unique_by=None, unique=False))
    def test_valid_return_value_covers_all_area(self, r):
        # if turn on all the light of given lamps, it shall cover all the area  

        # lamp_lights = min_lamp.min_lamp_solution(r) # return a list of index 
        lamp_lights = min_lamp.min_lamp_solution(r) # incorrect_min_lamp min_lamp_solution
        
        if lamp_lights!=None: 
            for lamp_on in lamp_lights: # lamp_on is index 
                self.assertTrue(lamp_on <= len(r)-1) # out of index 

            max_light = 0 
            for lamp_on in lamp_lights: # lamp_on is index 
                
                if lamp_lights.index(lamp_on) == 0:
                    if (lamp_on - r[lamp_on] <= 0): # first index 
                        max_light = lamp_on + r[lamp_on] # location + light
                        initial_not_cover = True  

                    else: 
                        initial_not_cover = False 
                
                # light covers the previous's max 
                elif (lamp_on - r[lamp_on]) <= max_light:
                    max_light = lamp_on + r[lamp_on]

            self.assertGreaterEqual(max_light, len(r)-1) and self.assertTrue(initial_not_cover)


    @given(st.lists(
        st.integers(min_value=0, max_value=5), 
        min_size=2, max_size=None, unique_by=None, unique=False))
    def test_turn_all_lamps_give_none(self, r):
        # if turn on all lights and there is an area where the area is not covered, the function shall 
            # return None   

        end_r = r.copy() # make a copy 

        for i in range(len(r)): # looping through the list 
            if r[i] != 0:
                for j in range(1, r[i]+1): 
                    if i+j <= len(r)-1: # avoid index error (end of the list)
                        end_r[i+j] += 1  
                    if i - j >= 0: # avoid index error (beginning of the list)
                        end_r[i-j] += 1 
        
        if 0 in end_r: # if there is zero, shall return None 
            # print(r, end_r) 
            self.assertEqual(min_lamp.incorrect_min_lamp(r), None)

    
    @given(st.lists(
                st.integers(min_value=0, max_value=5), 
                min_size=2, max_size=None, unique_by=None, unique=False))
    def test_time_complexity(self, r):
        # time complexity has to be O(nlogn)
        # doesnt generate a high number. It always starts small and doesnt go really high. 
        # The idea of testing time complexity might not be a good idea. 
        # It looks like a linear but it's actuall nlogn. People online 
        with open("x", "rb") as file:
            plot_data_x = pickle.load(file)
        
        with open("y", 'rb') as file:
            plot_data_y = pickle.load(file)

        start = time.time_ns()
        min_lamp.min_lamp_solution(r)
        end = time.time_ns() 

        plot_data_x.append(len(r)) # length 
        plot_data_y.append((end - start)/1000) # time 
        # print(plot_data_x, plot_data_y)

        with open("x", "wb") as file:
            pickle.dump(plot_data_x, file, protocol=pickle.HIGHEST_PROTOCOL)
        
        with open("y", 'wb') as file:
            pickle.dump(plot_data_y, file, protocol=pickle.HIGHEST_PROTOCOL)

    def tearDown(self):
        with open("x", "rb") as file:
            plot_data_x = pickle.load(file)
        
        with open("y", 'rb') as file:
            plot_data_y = pickle.load(file)
        
        plt.xlim([0, 200])
        plt.ylim([0, 200])
        plt.xticks(range(0, 200, 5))
        plt.yticks(range(0, 200, 5))
        plt.plot(plot_data_x, plot_data_y, 'o')
        plt.show()

if __name__ == '__main__':

    # resets to empty list every time 
    with open("x", 'wb+') as file:
        pickle.dump([], file, protocol=pickle.HIGHEST_PROTOCOL)

    with open("y", 'wb+') as file:
        pickle.dump([], file, protocol=pickle.HIGHEST_PROTOCOL)
    
    unittest.main()
