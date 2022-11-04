# POKER

from util import *
import random
import math
import copy


class CardCombination():
    def __init__(self, cards):
        self.cards = cards
    
    def combination(self):
        if len(self.cards) < 1:
            return CardCombination.combinations[-1]
        
        num_count = self.count_nums()

        flush_high = self.highest_card_index_in_flush()
        flush = flush_high > 0

        straight_high = self.highest_card_index_in_straight()
        straight = straight_high > 0

        flush_straight_high = -1

        if flush and straight:
            if flush_high == 1 or straight_high == 1:
                flush_straight_high = max(flush_high, straight_high)
            else:
                flush_straight_high = min(flush_high, straight_high)

        flush_straight = flush_straight_high > 0

        if flush_straight:         
            # Check for RSF and SF
            fsh_modified = flush_straight_high
            if flush_straight_high == 1:
                fsh_modified = 14
            
            straight_indicies = [
                fsh_modified - 4,
                fsh_modified - 3,
                fsh_modified - 2,
                fsh_modified - 1,
                flush_straight_high
            ]

            straight_cards = []
            flush_shape = Card.shapes[-1]

            for c in self.cards:
                # Try to make a straight flush
                if c.num_index() == straight_indicies[0]:
                    straight_cards.append(c)
                    flush_shape = c.shape

                    second_card = False
                    for c2 in self.cards:
                        if c2.num_index() == straight_indicies[1] and c2.shape == flush_shape:
                            straight_cards.append(c2)
                            second_card = True

                    if second_card == False:
                        straight_cards.clear()
                        flush_shape = Card.shapes[-1]
                    else:
                        third_card = False
                        for c3 in self.cards:
                            if c3.num_index() == straight_indicies[2] and c3.shape == flush_shape:
                                straight_cards.append(c3)
                                third_card = True
                        
                        if third_card == False:
                            straight_cards.clear()
                            flush_shape = Card.shapes[-1]
                        else:
                            fourth_card = False
                            for c4 in self.cards:
                                if c4.num_index() == straight_indicies[3] and c4.shape == flush_shape:
                                    straight_cards.append(c4)
                                    fourth_card = True
                            
                            if fourth_card == False:
                                straight_cards.clear()
                                flush_shape = Card.shapes[-1]
                            else:
                                fifth_card = False
                                for c5 in self.cards:
                                    if c5.num_index() == straight_indicies[4] and c5. shape == flush_shape:
                                        straight_cards.append(c5)
                                        fifth_card = True
                                
                                if fifth_card == False:
                                    straight_cards.clear()
                                    flush_shape = Card.shapes[-1]
            if len(straight_cards) >= 5:
                if straight_cards[-1].num_index() == 1:
                    return CardCombination.combinations[9] # RSF eliminated
                else:
                    return CardCombination.combinations[8] # SF eliminated
        else:
            for nc in num_count.keys():
                if num_count[nc] >= 4:
                    return CardCombination.combinations[7]  # FoaK eliminated
                elif num_count[nc] >= 3:
                    num_count_2 = self.count_nums()
                    del(num_count_2[nc])
                    for nc2 in num_count_2:
                        if num_count_2[nc2] >= 2:
                            return CardCombination.combinations[6] # Full House eliminated
        
        if flush:
            return CardCombination.combinations[5] # Flush eliminated

        if straight:
            return CardCombination.combinations[4] # Straight eliminated

        for nc in num_count.keys():
            if num_count[nc] >= 3:
                return CardCombination.combinations[3] # ToaK eliminated
            elif num_count[nc] >= 2:
                num_count_2 = self.count_nums()
                del num_count_2[nc]
                for nc2 in num_count_2:
                    if num_count_2[nc2] >= 2:
                        return CardCombination.combinations[2] # Two Pairs eliminated
                return CardCombination.combinations[1] # One Pair eliminated
        
        return CardCombination.combinations[0]

    def combination_index(self):
        return get_index_of_dict_value(CardCombination.combinations, self.combination())

    def first_relevant_card_index(self):
        combination = self.combination()

        if combination == CardCombination.combinations[9]: # RSF
            return 1
        elif combination == CardCombination.combinations[8]: # SF
            highest_flush = self.highest_card_index_in_flush()
            highest_straight = self.highest_card_index_in_straight()

            if highest_flush == 1:
                highest_flush = 14
            if highest_straight == 1:
                highest_straight = 14
            
            highest_straight_flush = min(highest_flush, highest_straight)

            if highest_straight_flush == 14:
                highest_straight_flush = 1

            return highest_straight_flush
        elif combination == CardCombination.combinations[7]: # FoaK
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 4:
                    return index
        elif combination == CardCombination.combinations[6] or combination == CardCombination.combinations[3]: # Full House and ToaK
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 3:
                    return index
        elif combination == CardCombination.combinations[5]: # Flush
            return self.highest_card_index_in_flush()
        elif combination == CardCombination.combinations[4]: # Straight
            return self.highest_card_index_in_straight()
        elif combination == CardCombination.combinations[2] or combination == CardCombination.combinations[1]: # Two Pairs and One Pair
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 2:
                    return index
        elif combination == CardCombination.combinations[0]: # High Card
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 1:
                    return index
        else:
            return -1

    def second_relevant_card_index(self):
        combination = self.combination()

        if combination == CardCombination.combinations[9]: # RSF
            return 13
        elif combination == CardCombination.combinations[8]: # SF
            highest_flush = self.highest_card_index_in_flush()
            highest_straight = self.highest_card_index_in_straight()

            if highest_flush == 1:
                highest_flush = 14
            if highest_straight == 1:
                highest_straight = 14
            
            highest_straight_flush = min(highest_flush, highest_straight) - 1

            if highest_straight_flush == 14:
                highest_straight_flush = 1

            return highest_straight_flush
        elif combination == CardCombination.combinations[7]: # FoaK
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 4:
                    return index
        elif combination == CardCombination.combinations[6] or combination == CardCombination.combinations[3]: # Full House and ToaK
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 3:
                    return index
        elif combination == CardCombination.combinations[5]: # Flush
            shape_count = self.count_shapes()
            shapes = []
            for sc in shape_count.keys():
                if shape_count[sc] >= 5:
                    shapes.append(Card.shapes[sc])
            
            index = -1
            for s in shapes:
                cards = []
                for c in self.cards:
                    if c.shape == s:
                        cards.append(copy.deepcopy(c))

                cards_contains_highest_index = False

                for c in cards:
                    if c.num_index() == self.highest_card_index_in_flush():
                        cards_contains_highest_index = True
                
                if cards_contains_highest_index == False:
                    break
                
                card_combination = CardCombination(cards)
                card_combination.cards.remove(card_combination.highest_card_by_index())

                highest_card_index = card_combination.highest_card_by_index().num_index()
                if highest_card_index == 1:
                    highest_card_index = 14
                index = max(index, highest_card_index)
            
            if index == 14:
                index = 1
            return index
        elif combination == CardCombination.combinations[4]: # Straight
            return self.highest_card_index_in_straight() - 1
        elif combination == CardCombination.combinations[2] or combination == CardCombination.combinations[1]: # Two pairs and One Pair
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 2:
                    return index
        elif combination == CardCombination.combinations[0]: # High Card
            num_count = self.count_nums()
            cards = copy.deepcopy(self.cards)

            cards.remove(CardCombination(cards).highest_card_by_index())

            return CardCombination(cards).highest_card_by_index().num_index()
        else:
            return -1

    def third_relevant_card_index(self):
        combination = self.combination()

        if combination == CardCombination.combinations[9]: # RSF
            return 12
        elif combination == CardCombination.combinations[8]: # SF
            highest_flush = self.highest_card_index_in_flush()
            highest_straight = self.highest_card_index_in_straight()

            if highest_flush == 1:
                highest_flush = 14
            if highest_straight == 1:
                highest_straight = 14
            
            highest_straight_flush = min(highest_flush, highest_straight) - 2

            if highest_straight_flush == 14:
                highest_straight_flush = 1

            return highest_straight_flush
        elif combination == CardCombination.combinations[7]: # FoaK
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 4:
                    return index
        elif combination == CardCombination.combinations[6] or combination == CardCombination.combinations[3]: # Full House and ToaK
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 3:
                    return index
        elif combination == CardCombination.combinations[5]: # Flush
            shape_count = self.count_shapes()
            shapes = []
            for sc in shape_count.keys():
                if shape_count[sc] >= 5:
                    shapes.append(Card.shapes[sc])
            
            index = -1
            for s in shapes:
                cards = []
                for c in self.cards:
                    if c.shape == s:
                        cards.append(copy.deepcopy(c))

                cards_contains_highest_index = False

                for c in cards:
                    if c.num_index() == self.highest_card_index_in_flush():
                        cards_contains_highest_index = True
                
                if cards_contains_highest_index == False:
                    break
                
                card_combination = CardCombination(cards)
                card_combination.cards.remove(card_combination.highest_card_by_index())
                card_combination.cards.remove(card_combination.highest_card_by_index())

                highest_card_index = card_combination.highest_card_by_index().num_index()
                if highest_card_index == 1:
                    highest_card_index = 14
                index = max(index, highest_card_index)
            
            if index == 14:
                index = 1
            return index
        elif combination == CardCombination.combinations[4]: # Straight
            return self.highest_card_index_in_straight() - 2
        elif combination == CardCombination.combinations[2]: # Two Pairs
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 2:
                    cards = copy.deepcopy(self.cards)
                    remove_cards = []
                    for c in cards:
                        if c.num_index() == index:
                            remove_cards.append(c)
                    
                    for rc in remove_cards:
                        cards.remove(rc)
                    
                    return CardCombination(cards).first_relevant_card_index()
        elif combination == CardCombination.combinations[1]: # One Pair
            num_count = self.count_nums()
            cards = copy.deepcopy(self.cards)

            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1

                if num_count[index] >= 2:
                    remove_cards = []
                    for c in cards:
                        if c.num_index() == index:
                            remove_cards.append(c)
                    
                    for rc in remove_cards:
                        cards.remove(rc)

            return CardCombination(cards).highest_card_by_index().num_index()
        elif combination == CardCombination.combinations[0]: # High Card
            num_count = self.count_nums()
            cards = copy.deepcopy(self.cards)

            cards.remove(CardCombination(cards).highest_card_by_index())
            cards.remove(CardCombination(cards).highest_card_by_index())

            return CardCombination(cards).highest_card_by_index().num_index()
        else:
            return -1
            
    def fourth_relevant_card_index(self):
        combination = self.combination()

        if combination == CardCombination.combinations[9]: # RSF
            return 11
        elif combination == CardCombination.combinations[8]: # SF
            highest_flush = self.highest_card_index_in_flush()
            highest_straight = self.highest_card_index_in_straight()

            if highest_flush == 1:
                highest_flush = 14
            if highest_straight == 1:
                highest_straight = 14
            
            highest_straight_flush = min(highest_flush, highest_straight) - 3

            if highest_straight_flush == 14:
                highest_straight_flush = 1

            return highest_straight_flush
        elif combination == CardCombination.combinations[7]: # FoaK
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 4:
                    return index
        elif combination == CardCombination.combinations[6]: # Full House
            num_count = self.count_nums()
            three_card_index = -1
            for i in range(1, 15):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 3:
                    three_card_index = index
            
            num_count[three_card_index] = 0

            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1

                if num_count[index] > 1:
                    return index
        elif combination == CardCombination.combinations[5]: # Flush
            shape_count = self.count_shapes()
            shapes = []
            for sc in shape_count.keys():
                if shape_count[sc] >= 5:
                    shapes.append(Card.shapes[sc])
            
            index = -1
            for s in shapes:
                cards = []
                for c in self.cards:
                    if c.shape == s:
                        cards.append(copy.deepcopy(c))

                cards_contains_highest_index = False

                for c in cards:
                    if c.num_index() == self.highest_card_index_in_flush():
                        cards_contains_highest_index = True
                
                if cards_contains_highest_index == False:
                    break
                
                card_combination = CardCombination(cards)
                card_combination.cards.remove(card_combination.highest_card_by_index())
                card_combination.cards.remove(card_combination.highest_card_by_index())
                card_combination.cards.remove(card_combination.highest_card_by_index())

                highest_card_index = card_combination.highest_card_by_index().num_index()
                if highest_card_index == 1:
                    highest_card_index = 14
                index = max(index, highest_card_index)
            
            if index == 14:
                index = 1
            return index
        elif combination == CardCombination.combinations[4]: # Straight
            return self.highest_card_index_in_straight() - 3
        elif combination == CardCombination.combinations[3]: # ToaK
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 3:
                    cards = copy.deepcopy(self.cards)
                    remove_cards = []
                    for c in cards:
                        if c.num_index() == index:
                            remove_cards.append(c)
                    
                    for rc in remove_cards:
                        cards.remove(rc)
                    
                    return CardCombination(cards).highest_card_by_index().num_index()
        elif combination == CardCombination.combinations[2]: # Two Pairs
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 2:
                    cards = copy.deepcopy(self.cards)
                    remove_cards = []
                    for c in cards:
                        if c.num_index() == index:
                            remove_cards.append(c)
                    
                    for rc in remove_cards:
                        cards.remove(rc)
                    
                    return CardCombination(cards).first_relevant_card_index()
        elif combination == CardCombination.combinations[1]: # One Pair
            num_count = self.count_nums()
            cards = copy.deepcopy(self.cards)

            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1

                if num_count[index] >= 2:
                    remove_cards = []
                    for c in cards:
                        if c.num_index() == index:
                            remove_cards.append(c)
                    
                    for rc in remove_cards:
                        cards.remove(rc)
            
            cards.remove(CardCombination(cards).highest_card_by_index())

            return CardCombination(cards).highest_card_by_index().num_index()
        elif combination == CardCombination.combinations[0]: # High Card
            num_count = self.count_nums()
            cards = copy.deepcopy(self.cards)

            cards.remove(CardCombination(cards).highest_card_by_index())
            cards.remove(CardCombination(cards).highest_card_by_index())
            cards.remove(CardCombination(cards).highest_card_by_index())

            return CardCombination(cards).highest_card_by_index().num_index()
        else:
            return -1

    def fifth_relevant_card_index(self):
        combination = self.combination()

        if combination == CardCombination.combinations[9]: # RSF
            return 10
        elif combination == CardCombination.combinations[8]: # SF
            highest_flush = self.highest_card_index_in_flush()
            highest_straight = self.highest_card_index_in_straight()

            if highest_flush == 1:
                highest_flush = 14
            if highest_straight == 1:
                highest_straight = 14
            
            highest_straight_flush = min(highest_flush, highest_straight) - 4

            if highest_straight_flush == 14:
                highest_straight_flush = 1

            return highest_straight_flush
        elif combination == CardCombination.combinations[7]: # FoaK
            num_count = self.count_nums()
            four_card_index = -1
            for i in range(1, 15):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 4:
                    four_card_index = index
            
            num_count[four_card_index] = 0

            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1

                if num_count[index] > 0:
                    return index
        elif combination == CardCombination.combinations[6]: # Full House
            num_count = self.count_nums()
            three_card_index = -1
            for i in range(1, 15):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 3:
                    three_card_index = index
            
            num_count[three_card_index] = 0

            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1

                if num_count[index] > 1:
                    return index
        elif combination == CardCombination.combinations[5]: # Flush
            shape_count = self.count_shapes()
            shapes = []
            for sc in shape_count.keys():
                if shape_count[sc] >= 5:
                    shapes.append(Card.shapes[sc])
            
            index = -1
            for s in shapes:
                cards = []
                for c in self.cards:
                    if c.shape == s:
                        cards.append(copy.deepcopy(c))

                cards_contains_highest_index = False

                for c in cards:
                    if c.num_index() == self.highest_card_index_in_flush():
                        cards_contains_highest_index = True
                
                if cards_contains_highest_index == False:
                    break
                
                card_combination = CardCombination(cards)
                card_combination.cards.remove(card_combination.highest_card_by_index())
                card_combination.cards.remove(card_combination.highest_card_by_index())
                card_combination.cards.remove(card_combination.highest_card_by_index())
                card_combination.cards.remove(card_combination.highest_card_by_index())

                highest_card_index = card_combination.highest_card_by_index().num_index()
                if highest_card_index == 1:
                    highest_card_index = 14
                index = max(index, highest_card_index)
            
            if index == 14:
                index = 1
            return index
        elif combination == CardCombination.combinations[4]: # Straight
            return self.highest_card_index_in_straight() - 4
        elif combination == CardCombination.combinations[3]: # ToaK
            num_count = self.count_nums()
            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1
                
                if num_count[index] >= 3:
                    cards = copy.deepcopy(self.cards)
                    remove_cards = []
                    for c in cards:
                        if c.num_index() == index:
                            remove_cards.append(c)
                    
                    for rc in remove_cards:
                        cards.remove(rc)
                    
                    cards.remove(CardCombination(cards).highest_card_by_index())
                    return CardCombination(cards).highest_card_by_index().num_index()
        elif combination == CardCombination.combinations[2]: # Two Pairs
            num_count = self.count_nums()
            cards = copy.deepcopy(self.cards)

            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1

                if num_count[index] >= 2:
                    remove_cards = []
                    for c in cards:
                        if c.num_index() == index:
                            remove_cards.append(c)
                    
                    for rc in remove_cards:
                        cards.remove(rc)
                
            return CardCombination(cards).highest_card_by_index().num_index()
        elif combination == CardCombination.combinations[1]: # One Pair
            num_count = self.count_nums()
            cards = copy.deepcopy(self.cards)

            for i in range(14, 0, -1):
                index = i
                if i == 14:
                    index = 1

                if num_count[index] >= 2:
                    remove_cards = []
                    for c in cards:
                        if c.num_index() == index:
                            remove_cards.append(c)
                    
                    for rc in remove_cards:
                        cards.remove(rc)
            
            cards.remove(CardCombination(cards).highest_card_by_index())
            cards.remove(CardCombination(cards).highest_card_by_index())

            return CardCombination(cards).highest_card_by_index().num_index()
        elif combination == CardCombination.combinations[0]: # High Card
            num_count = self.count_nums()
            cards = copy.deepcopy(self.cards)

            cards.remove(CardCombination(cards).highest_card_by_index())
            cards.remove(CardCombination(cards).highest_card_by_index())
            cards.remove(CardCombination(cards).highest_card_by_index())
            cards.remove(CardCombination(cards).highest_card_by_index())

            return CardCombination(cards).highest_card_by_index().num_index()
        else:
            return -1

    def highest_card_index_in_straight(self):
        highest_card_index = -1
        num_count = self.count_nums()
        
        # Adds Aces to the right
        num_count[14] = num_count[1]
        
        # Checks for straight
        for i in range(5, 15):
            if num_count[i] > 0:
                if num_count[i - 1] > 0:
                    if num_count[i - 2] > 0:
                        if num_count[i - 3] > 0:
                            if num_count[i - 4] > 0:
                                highest_card_index = i

        if highest_card_index == 14:
            highest_card_index = 1

        return highest_card_index
    
    def highest_card_index_in_flush(self):
        highest_card_index = -1

        # Removes shapes that aren't a flush
        shape_count = self.count_shapes()
        del_indicies = []
        for sc in shape_count.keys():
            if shape_count[sc] < 5:
                del_indicies.append(sc)
        for i in del_indicies:
            del shape_count[i]

        # Gets highest flush card
        for sc in shape_count.keys():
            for c in self.cards:
                # Move Aces to the right
                i_modified = c.num_index()
                if i_modified == 1:
                    i_modified = 14

                if c.shape == Card.shapes[sc] and i_modified > highest_card_index:
                    highest_card_index = i_modified

        if highest_card_index == 14:
            highest_card_index = 1

        return highest_card_index
    
    def count_shapes(self):
        shape_count = {
            -1 : 0,
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0
        }

        for c in self.cards:
            shape_count[c.shape_index()] += 1
        
        return shape_count
    
    def count_nums(self):
        num_count = {
            -1 : 0,
            1 : 0,
            2 : 0,
            3 : 0,
            4 : 0,
            5 : 0,
            6 : 0,
            7 : 0,
            8 : 0,
            9 : 0,
            10 : 0,
            11 : 0,
            12 : 0,
            13 : 0
        }
        
        for c in self.cards:
            num_count[c.num_index()] += 1
        
        return num_count              

    def is_better_than(self, comb):
        ci1 = self.combination_index()
        ci2 = comb.combination_index()
        if ci1 > ci2:
            return True
        elif ci1 == ci2:
            c1 = self.first_relevant_card_index()
            c2 = comb.first_relevant_card_index()

            if c1 == 1:
                c1 = 14
            if c2 == 1:
                c2 = 14

            if c1 > c2:
                return True
            elif c1 == c2:
                c1_2 = self.second_relevant_card_index()
                c2_2 = comb.second_relevant_card_index()

                if c1_2 == 1:
                    c1_2 = 14
                if c2_2 == 1:
                    c2_2 = 14

                if c1_2 > c2_2:
                    return True
                elif c1_2 == c1_2:
                    c1_3 = self.third_relevant_card_index()
                    c2_3 = comb.third_relevant_card_index()

                    if c1_3 == 1:
                        c1_3 = 14
                    if c2_3 == 1:
                        c2_3 = 14
                    
                    if c1_3 > c2_3:
                        return True
                    elif c1_3 == c2_3:
                        c1_4 = self.fourth_relevant_card_index()
                        c2_4 = comb.fourth_relevant_card_index()

                        if c1_4 == 1:
                            c1_4 = 14
                        if c2_4 == 1:
                            c2_4 = 14
                        
                        if c1_4 > c2_4:
                            return True
                        elif c1_4 == c2_4:
                            c1_5 = self.fifth_relevant_card_index()
                            c2_5 = comb.fifth_relevant_card_index()

                            if c1_5 == 1:
                                c1_5 = 14
                            if c2_5 == 1:
                                c2_5 = 14
                            
                            if c1_5 > c2_5:
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def is_equal_to(self, comb):
        ci1 = self.combination_index()
        ci2 = comb.combination_index()
        if ci1 == ci2:
            c1 = self.first_relevant_card_index()
            c2 = comb.first_relevant_card_index()

            if c1 == c2:
                c1_2 = self.second_relevant_card_index()
                c2_2 = comb.second_relevant_card_index()

                if c1_2 == c2_2:
                    c1_3 = self.third_relevant_card_index()
                    c2_3 = comb.third_relevant_card_index()
                    

                    if c1_3 == c2_3:
                        c1_4 = self.fourth_relevant_card_index()
                        c2_4 = comb.fourth_relevant_card_index()

                        if c1_4 == c2_4:
                            c1_5 = self.fifth_relevant_card_index()
                            c2_5 = comb.fifth_relevant_card_index()
                            
                            if c1_5 == c2_5:
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def is_worse_than(self, comb):
        ge = self.is_better_than(comb) or self.is_equal_to(comb)
        return not ge

    def highest_card_by_index(self):
        highest_index = -1

        for c in self.cards:
            card_index = c.num_index()
            if card_index == 1:
                card_index = 14
            
            highest_index = max(card_index, highest_index)
        
        if highest_index == 14:
            highest_index = 1
        
        for c in self.cards:
            if c.num_index() == highest_index:
                return c

    combinations = {
        -1: "error",
        0 : "high card",
        1 : "one pair",
        2 : "two pairs",
        3 : "three of a kind",
        4 : "straight",
        5 : "flush",
        6 : "full house",
        7 : "four of a kind",
        8 : "straight flush",
        9 : "royal straight flush"
    }


class Card():
    def __init__(self, num, shape):
        self.num = num
        self.shape = shape
    
    def shape_index(self):
        return get_index_of_dict_value(self.shapes, self.shape)
    
    def num_index(self):
        return get_index_of_dict_value(Card.nums, self.num)

    shapes = {
        -1: "error",
        0 : "spade",
        1 : "diamond",
        2 : "clover",
        3 : "heart"
    }

    nums = {
        -1: "error",
        1 : "ace",
        2 : "deuce",
        3 : "three",
        4 : "four",
        5 : "five",
        6 : "six",
        7 : "seven",
        8 : "eight",
        9 : "nine",
        10 : "ten",
        11 : "jack",
        12 : "queen",
        13 : "king"
    }

    def display_name(self):
        return self.num.capitalize() + " of " + self.shape.capitalize() + "s"

    def deck():
        return list(Card.deck_as_dict().values())
    
    def deck_as_dict():
        deck = {
            "AS" : Card(Card.nums[1], Card.shapes[0]),
            "DS" : Card(Card.nums[2], Card.shapes[0]),
            "TS" : Card(Card.nums[3], Card.shapes[0]),
            "CS" : Card(Card.nums[4], Card.shapes[0]),
            "FS" : Card(Card.nums[5], Card.shapes[0]),
            "HS" : Card(Card.nums[6], Card.shapes[0]),
            "SS" : Card(Card.nums[7], Card.shapes[0]),
            "ES" : Card(Card.nums[8], Card.shapes[0]),
            "NS" : Card(Card.nums[9], Card.shapes[0]),
            "XS" : Card(Card.nums[10], Card.shapes[0]),
            "JS" : Card(Card.nums[11], Card.shapes[0]),
            "QS" : Card(Card.nums[12], Card.shapes[0]),
            "KS" : Card(Card.nums[13], Card.shapes[0]),
            "AD" : Card(Card.nums[1], Card.shapes[1]),
            "DD" : Card(Card.nums[2], Card.shapes[1]),
            "TD" : Card(Card.nums[3], Card.shapes[1]),
            "CD" : Card(Card.nums[4], Card.shapes[1]),
            "FD" : Card(Card.nums[5], Card.shapes[1]),
            "HD" : Card(Card.nums[6], Card.shapes[1]),
            "SD" : Card(Card.nums[7], Card.shapes[1]),
            "ED" : Card(Card.nums[8], Card.shapes[1]),
            "ND" : Card(Card.nums[9], Card.shapes[1]),
            "XD" : Card(Card.nums[10], Card.shapes[1]),
            "JD" : Card(Card.nums[11], Card.shapes[1]),
            "QD" : Card(Card.nums[12], Card.shapes[1]),
            "KD" : Card(Card.nums[13], Card.shapes[1]),
            "AC" : Card(Card.nums[1], Card.shapes[2]),
            "DC" : Card(Card.nums[2], Card.shapes[2]),
            "TC" : Card(Card.nums[3], Card.shapes[2]),
            "CC" : Card(Card.nums[4], Card.shapes[2]),
            "FC" : Card(Card.nums[5], Card.shapes[2]),
            "HC" : Card(Card.nums[6], Card.shapes[2]),
            "SC" : Card(Card.nums[7], Card.shapes[2]),
            "EC" : Card(Card.nums[8], Card.shapes[2]),
            "NC" : Card(Card.nums[9], Card.shapes[2]),
            "XC" : Card(Card.nums[10], Card.shapes[2]),
            "JC" : Card(Card.nums[11], Card.shapes[2]),
            "QC" : Card(Card.nums[12], Card.shapes[2]),
            "KC" : Card(Card.nums[13], Card.shapes[2]),
            "AH" : Card(Card.nums[1], Card.shapes[3]),
            "DH" : Card(Card.nums[2], Card.shapes[3]),
            "TH" : Card(Card.nums[3], Card.shapes[3]),
            "CH" : Card(Card.nums[4], Card.shapes[3]),
            "FH" : Card(Card.nums[5], Card.shapes[3]),
            "HH" : Card(Card.nums[6], Card.shapes[3]),
            "SH" : Card(Card.nums[7], Card.shapes[3]),
            "EH" : Card(Card.nums[8], Card.shapes[3]),
            "NH" : Card(Card.nums[9], Card.shapes[3]),
            "XH" : Card(Card.nums[10], Card.shapes[3]),
            "JH" : Card(Card.nums[11], Card.shapes[3]),
            "QH" : Card(Card.nums[12], Card.shapes[3]),
            "KH" : Card(Card.nums[13], Card.shapes[3])
        }

        return deck


class Game():
    def __init__(self, sb, bb, ante):
        self.stage = Game.stages[-1]
        self.deck = Card.deck()
        self.dealer = -1
        self.pot = 0
        self.small_blind = sb
        self.big_blind = bb
        self.ante = ante
        self.board = []
        self.players = []
        self.dead_players = []

    def initialize(self):
        self.deck = Card.deck()
        self.dealer = self.players[random.randrange(0, len(self.players) - 1)]
        self.pot = 0
        self.dead_players.clear()
        self.collect_blinds()
        for p in self.players:
            p.raise_amount = 0
            p.paid = 0

    def collect_blinds(self):
        sb_player = self.next_player(self.dealer)
        bb_player = self.next_player(sb_player)

        sb_player.bankroll -= self.small_blind
        sb_player.paid += self.small_blind
        self.pot += self.small_blind

        bb_player.bankroll -= self.big_blind
        bb_player.bankroll -= self.ante
        bb_player.paid += self.big_blind
        self.pot += self.big_blind
        self.pot += self.ante
    
    def next_player(self, player):
        max_index = len(self.players) - 1
        next_index = self.players.index(player) + 1
        if next_index > max_index:
            next_index = 0
        
        return self.players[next_index]
        
    def proceed_stage(self):
        next_stage = self.next_stage()

        if next_stage == Game.stages[0]:
            self.initialize()
            self.deal_cards()
            self.collect_bets(self.big_blind, next_stage, 2)
            if len(self.players) - len(self.dead_players) <= 1:
                self.stage = Game.stages[3]
        elif next_stage == Game.stages[1]:
            for i in range(0, 3):
                self.board.append(copy.deepcopy(self.deck[i]))
                self.deck.remove(self.deck[i])
            self.collect_bets(0, next_stage)
            if len(self.players) - len(self.dead_players) <= 1:
                self.stage = Game.stages[3]
        elif next_stage == Game.stages[2] or next_stage == Game.stages[3]:
            self.board.append(copy.deepcopy(self.deck[0]))
            self.deck.remove(self.deck[0])
            self.collect_bets(0, next_stage)
            if len(self.players) - len(self.dead_players) <= 1:
                self.stage = Game.stages[3]
        elif next_stage == Game.stages[4]:
            winners = []
            highest_comb_index = -1
            highest_comb = CardCombination(self.board)

            for p in self.players:
                if p not in self.dead_players:
                    comb = CardCombination(p.hand)
                    for c in self.board:
                        comb.cards.append(copy.deepcopy(c))

                    if comb.is_better_than(highest_comb):
                        highest_comb = copy.deepcopy(comb)
                    

            for p in self.players:
                if p not in self.dead_players:
                    comb = CardCombination(p.hand)
                    for c in self.board:
                        comb.cards.append(copy.deepcopy(c))

                    if comb.is_better_than(highest_comb) or comb.is_equal_to(highest_comb):
                        winners.append(p)
            
            winning_amount = self.pot / len(winners)
            for w in winners:
                print(str(w.name) + " won " + str(winning_amount))
                self.pot -= winning_amount
                w.bankroll += winning_amount
            self.pot = 0
        
        self.stage = next_stage
        # TODO Main, second, third pot needs to be coded in
        # TODO Minimum chip value needs to be coded in
        # TODO Rakes
    
    def combination_of_player(self, player):
        if player in self.players:
            cards = copy.deepcopy(player.hand)
            for b in self.board:
                cards.append(b)
            return CardCombination(cards)
        else:
            return CardCombination(player.hand)
                
    def deal_cards(self):
        dealable_cards = len(self.deck) - 8
        max_players = math.floor(dealable_cards / 2)
        if len(self.players) <= max_players:
            random.shuffle(self.deck)

            i = 0

            for p in self.players:
                p.hand.clear()
                p.hand.append(self.deck[i])
                i += 1
            
            for p in self.players:
                p.hand.append(self.deck[i])
                i += 1

            for x in range(0, i - 1):
                self.deck.remove(self.deck[x])
            
            return True
        else:
            return False
    
    # TODO Differentiation between "raise to" and "raise" needs to be coded in
    # TODO Raise initiation player still as action
    def collect_bets(self, minimum_bet, stage, starting_player = 0):
        min_bet = minimum_bet
        last_action = Player.actions[-1]
        raise_occured = True

        player_queue_index = []
        for pqi in range(0, len(self.players)):
            player_queue_index.append(pqi)

        for pq in player_queue_index:
            pq += starting_player

            for offset in range(0, starting_player):
                if pq == len(self.players) + offset:
                    pq = offset
        
        player_queue = []
        for pqi in player_queue_index:
            player_queue.append(self.players[pqi])
        
        while raise_occured:
            raise_occured = False

            for p in player_queue:
                if len(self.players) - len(self.dead_players) <= 1:
                    break
                if p not in self.dead_players:
                    action = p.action(min_bet, stage, self.board)

                    # Player folds
                    if action == Player.actions[0]:
                        self.dead_players.append(p)
                        last_action = Player.actions[0]
                    # Player checks (will fold if player paid less than minimum bet)
                    elif action == Player.actions[1]:
                        if (min_bet - p.paid) > 0:
                            self.dead_players.append(p)
                            last_action = Player.actions[0]
                        else:
                            last_action = Player.actions[1]
                    # Player calls
                    elif action == Player.actions[2]:
                        p.bankroll -= (min_bet - p.paid)
                        self.pot += (min_bet - p.paid)
                        last_action = Player.actions[2]
                    # Player raises (will call if amount is an underbet)
                    elif action == Player.actions[3]:
                        can_raise = False
                        if p.raise_amount == p.bankroll:
                            can_raise = True
                            self.dead_players.append(p)
                        elif (p.raise_amount + p.paid) >= min_bet * 2:
                            can_raise = True
                        
                        if can_raise:
                            min_bet = (p.raise_amount + p.paid)
                            p.bankroll -= p.raise_amount
                            self.pot += p.raise_amount
                            last_action = Player.actions[3]
                            raise_occured = True
                        else:
                            p.bankroll -= min_bet
                            self.pot += min_bet
                            last_action = Player.actions[2]

    def next_stage(self):
        if self.stage == Game.stages[0]:
            return Game.stages[1]
        elif self.stage == Game.stages[1]:
            return Game.stages[2]
        elif self.stage == Game.stages[2]:
            return Game.stages[3]
        elif self.stage == Game.stages[3]:
            return Game.stages[4]
        else:
            return Game.stages[0]
    
    stages = {
        -1: "error",
        0 : "pre-flop",
        1 : "flop",
        2 : "turn",
        3 : "river",
        4 : "showdown"
    }


class Player():
    def __init__(self, name, bankroll):
        self.hand = []
        self.name = name
        self.bankroll = bankroll
        self.raise_amount = 0
        self.paid = 0
    
    def action(self, minimum_bet, stage, board):
        print("BOARD IS:")

        cards = []
        for c in board:
            print(c.display_name())
            cards.append(c)

        for h in self.hand:
            cards.append(h)
        print("CURRENT COMBINATION: " + str(CardCombination(cards).combination()) + " / " + Card.nums[CardCombination(cards).first_relevant_card_index()])
        
        print("==== " + self.name)
        print("CALL TO: " + str(minimum_bet))
        print("STAGE IS: " + str(stage))
        print("BANKROLL IS: " + str(self.bankroll))
        print("HAND IS: " + str(self.hand[0].display_name()) + " / " + str(self.hand[1].display_name()))
        print("0: FOLD\n1: CHECK\n2: CALL\n3: RAISE\n4: ALL IN")

        action_index = int(input("Action: "))

        if action_index == 3:
            self.raise_amount = int(input("RAISE TO: "))

        elif action_index == 4:
            self.raise_amount = self.bankroll
            action_index = 3

        return Player.actions[action_index]
    
    actions = {
        -1: "error",
        0 : "fold",
        1 : "check",
        2 : "call",
        3 : "raise"
    }






# RUNTIME

p1 = Player("Jack", 10000)
p2 = Player("Emma", 15000)

game = Game(100, 200, 200)
game.players = [
    p1,
    p2
]

while True:
    game.proceed_stage()