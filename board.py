from collections import defaultdict
from enum import Enum
import itertools
import random
from statistics import mean, pstdev

from data import DATA, RANK

# Resource clusters Max: 72 (can hit), Min: 49



class Tile:
    '''Represents a tile to be on the board'''

    def __init__(self, resource):
        self.resource = resource
        self.token = None

    def set_token(self, token):
        self.token = token


class Board:
    '''Represents an ordered collection of tiles'''

    def __init__(self, size, block_size='triplets', resource_clusters=None, token_clusters=None, resource_probabilities=None):
        '''
        Params:
            size: int | 4 or 6
            block_size: string | 'triplets' or 'septets'
            resource_clusters: string | 'low', 'med', or 'high'
            token_clusters: string | 'low', 'med', or 'high'
            resource_probabilities: string | 'low', 'med', or 'high'
        '''
        self.data = DATA[size]
        self.block_size = block_size
        self.resource_clusters = RANK.get(resource_clusters)
        self.token_clusters = RANK.get(token_clusters)
        self.resource_probabilities = RANK.get(resource_probabilities)

        self.tiles = []
        self.generate_matching()

    def generate_matching(self):
        # Max out at ten thousand calculations
        for x in range(10000):
            self.generate_random()
            if self.resource_clusters is not None:
                # Check if score is in range. if don't match, continue to next iteration of loop
                ranges = self.data[self.block_size]['resource_spacing_ranges'][self.resource_clusters]
                if not ranges[0] < self._calc_resource_clusters() < ranges[1]:
                    continue
            if self.token_clusters is not None:
                ranges = self.data[self.block_size]['token_spacing_ranges'][self.resource_clusters]
                if not ranges[0] < self._calc_token_clusters() < ranges[1]:
                    continue
            if self.resource_probabilities is not None:
                ranges = self.data[self.block_size]['resource_probability_ranges'][self.resource_clusters]
                
                pass
            print(x)
            return
        # If no matches make board empty
        self.tiles = []


    def generate_random(self):
        '''Generate a random board'''
        
        self.tiles = [Tile(resource) for resource in self._shuffle(self.data['resources'])]
        shuffled_tokens = self._shuffle(self.data['tokens'])
        for tile in self.tiles:
            if tile.resource == 'desert':
                tile.token = 7
            else:
                tile.token = shuffled_tokens.pop()

    def _shuffle(self, _list):
        return random.sample(_list, len(_list))

    def to_dict(self):
        return {'board': [tile.__dict__ for tile in self.tiles]}

    def _get_tile_groups(self, index_groups):
        return [[self.tiles[index] for index in index_group] for index_group in index_groups]

    def _calc_resource_clusters(self):
        '''Calculates resource cluster score. The lower the number, the fewer clusters'''
        tile_chunks = self._get_tile_groups(self.data[self.block_size]['tiles'])
        score = sum([
            abs(len(set([tile.resource for tile in tile_chunk])) - len(tile_chunk)) 
            for tile_chunk in tile_chunks
        ])
        return score

    def _calc_token_clusters(self):
        '''Calculates token cluster score. The lower the number, the fewer clusters'''
        tile_chunks = self._get_tile_groups(self.data[self.block_size]['tiles'])
        score = pstdev([
            round(mean([abs(tile.token - 7) for tile in tile_chunk]))
            for tile_chunk in tile_chunks
        ])
        return score

    def _calc_resource_probability(self):
        '''Calculates the probability of resources. The lower the number, the more even resources are'''
        bucketed = defaultdict(list)
        for tile in self.tiles:
            bucketed[tile.resource].append(abs(tile.token - 7))
        population = [mean(resource_probs) for resource_probs in bucketed.values()]
        return pstdev(population)
