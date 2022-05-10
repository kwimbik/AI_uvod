import numpy as np

cache = {}
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]
game_primes = []
tempList = []
#lists = np.array[20]

#Todo pole indexovane kameny s listem tahu
#seradit je vzdycky podle poctu navazujicich tahu od nejmensi a delat for loop v tomto poradi

def can_take(a, b):
    """
        Return True if a player can take a when b was played before
        Note that can_take(a, b) == can_take(b, a)
    """
    return a % b == 0 if a >= b else b % a == 0

def player(stones, last):
    """
        Return one move of the current player
        stones: A list of remaining numbers which have not been taken.
        last: A number taken in the last move.
        The function is expected to return one number which can be taken to win if the position is winning, and False if the position is loosing.

        TODO: Implement this function.
    """

    #primer fctio
    if stones == []: return []
    last_element = stones[len(stones)-1]
    #for prime in primes:
    #    if prime < last_element:
    #        game_primes.append(prime)
    #    else:
    #        break
    ## end of primes fction

    #sorted fction
    #global tempList
    #for stone in stones:
    #    count = 0
    #    for k in stones:
    #        if stone != k:
    #            if stone % k == 0 or k % stone == 0:
    #                count += 1
    #    tempList.append((stone, count))
    ##end of sortedfctio 
    #tempList = sorted(tempList, 
    #   key=lambda x: x[1])

    npStones = [0] * (last_element+1) #np.zeros(last_element+1)
    for s in stones:
        npStones[s] = 1
    win = firstPlayerWinning(last, npStones)
    if win == -1: return False
    return win


def firstPlayerWinning(lastStone, remainingStones):
        if (lastStone, hash(str(remainingStones))) in cache:
            return cache[lastStone, hash(str(remainingStones))]
        for stone in range(len(remainingStones) - 1, -1, -1):
            if remainingStones[stone] == 1 and can_take(stone, lastStone):
                remainingStones[stone] = 0
                if (firstPlayerWinning(stone, remainingStones) == (-1)):
                    remainingStones[stone] = 1
                    cache[lastStone, hash(str(remainingStones))] = stone
                    return stone
                remainingStones[stone] = 1
        cache[lastStone, hash(str(remainingStones))] = -1
        return -1
