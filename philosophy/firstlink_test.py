#!/usr/bin/env python3

import unittest

from firstlink import get_first_article_link

class FirstLinkTest(unittest.TestCase):

    base_url = 'https://en.wikipedia.org/wiki/'
    links_from_to = {
        'Turkish_language': 'Turkic_languages',
        'Siberia': 'Russian_language',
        'Baveh': 'Persian_language',
        'Rod_Levitt': 'Portland,_Oregon'
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

if __name__ == '__main__':
    unittest.main()
