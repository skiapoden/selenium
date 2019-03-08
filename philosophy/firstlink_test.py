#!/usr/bin/env python3

import unittest

from firstlink import get_first_article_link

class FirstLinkTest(unittest.TestCase):

    # TODO: wrap test case maps with different Wikipedia languages

    base_url = 'https://en.wikipedia.org/wiki/'
    links_from_to = {
        'Turkish_language': 'Turkic_languages',
        'Baveh': 'Persian_language',
        'Rod_Levitt': 'Portland,_Oregon',
        'Bristol_stool_scale': 'Medicine',
        'Kaiserschmarrn': 'Kaiser',
        'Sciapode': 'Paris',
        'Beer': 'Alcoholic_drink',
        'Glenn_Gould': 'Johann_Sebastian_Bach',
        'Oswald_Mosley': 'Member_of_parliament',
        'Semiconductor': 'Electrical_conductor'
    }

    def test_get_first_article_link(self):
        for source_article in self.links_from_to:
            # arrange
            article_url = self.base_url + source_article
            target_url = self.base_url + self.links_from_to[source_article]

            # act
            found_url = get_first_article_link(article_url)

            # assert
            self.assertEqual(target_url, found_url)

    stop_after_hops = 20
    target = 'https://en.wikipedia.org/wiki/Philosophy'
    distances = {
        'Social_science': 7,
        'Teacup': 12,
        'Worthy_Patterson': stop_after_hops,
    }

    def test_find_random_n_away_from_target(self):
        for source in self.distances:
            # arrange
            url = self.base_url + source

            # act
            hops = -1 # 0 after initial article is browsed
            while hops < self.stop_after_hops:
                url = get_first_article_link(url)
                hops += 1
                if url == self.target:
                    hops += 1 # target article is not browsed
                    break

            # assert
            expected = self.distances[source]
            self.assertEqual(hops, expected, '{} took {} hops, expected {}'.format(source, hops, expected))

if __name__ == '__main__':
    unittest.main()
