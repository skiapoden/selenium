#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import unittest

from firstlinkEE import get_first_article_link

class FirstLinkTest(unittest.TestCase):

    base_url_fmt = 'https://{}.wikipedia.org/wiki/{}'
    links_from_to = {
        'en': {
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
        },
        'de': {
            'Albert_Einstein': '14._M%C3%A4rz',
            'Königspfalz': 'Fr%C3%BChmittelalter',
            'Völkerwanderung': 'Migrationssoziologie'
        }
    }

    def test_get_first_article_link(self):
        for lang in self.links_from_to:
            for source_article in self.links_from_to[lang]:
                # arrange
                article_url = self.base_url_fmt.format(lang, source_article)
                target_url = self.base_url_fmt.format(lang, self.links_from_to[lang][source_article])

                # act
                found_url = get_first_article_link(article_url)

                # assert
                self.assertEqual(target_url, found_url)


    stop_after_hops = 20
    target_fmt = 'https://{}.wikipedia.org/wiki/{}'
    distances = {
        ('en', 'Philosophy'): {
            'Social_science': 7,
            'Teacup': 12,
            'Worthy_Patterson': stop_after_hops,
        },
        ('de', 'Philosophie'): {
            # TODO: find test cases that don't break the logic
        }
    }

    def test_find_random_n_away_from_target(self):
        for lang_target in self.distances:
            for source in self.distances[lang_target]:
                # arrange
                url = self.base_url_fmt.format(lang_target[0], source)

                # act
                hops = -1 # 0 after initial article is browsed
                while hops < self.stop_after_hops:
                    try:
                        url = get_first_article_link(url)
                    except Exception as e:
                        print(e)
                    hops += 1
                    if url == self.target_fmt.format(*lang_target):
                        hops += 1 # target article is not browsed
                        break

                # assert
                expected = self.distances[lang_target][source]
                self.assertEqual(hops, expected, '{} took {} hops, expected {}'.format(source, hops, expected))

if __name__ == '__main__':
    unittest.main()
