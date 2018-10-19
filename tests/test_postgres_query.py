import unittest

from alerta.database.backends.postgres.parser import query_parser


class PostgresQueryTestCase(unittest.TestCase):

    def setUp(self):

        pass

    def test_word_and_phrase_terms(self):

        # default field (ie. "text") contains word
        string = r'''quick'''
        r = query_parser(string)
        self.assertEqual(r, '"text" ILIKE \'%%quick%%\'')

        # default field (ie. "text") contains phrase
        string = r'''"quick brown"'''
        r = query_parser(string)
        self.assertEqual(r, '"text" ~* \'quick brown\'')

    def test_field_names(self):

        # field contains word
        string = r'''status:active'''
        r = query_parser(string)
        self.assertEqual(r, '"status" ILIKE \'%%active%%\'')

        # field contains either words
        string = r'''title:(quick OR brown)'''
        r = query_parser(string)
        self.assertEqual(r, '("title" ILIKE \'%%quick%%\' OR "title" ILIKE \'%%brown%%\')')

        # field contains either words (default operator)
        string = r'''title:(quick brown)'''
        r = query_parser(string)
        self.assertEqual(r, '("title" ILIKE \'%%quick%%\' OR "title" ILIKE \'%%brown%%\')')

        # field exact match
        string = r'''author:"John Smith"'''
        r = query_parser(string)
        self.assertEqual(r, '"author"=\'John Smith\'')

        # # any attribute contains word or phrase
        # string = r'''attributes.\*:(quick brown)'''
        # r = query_parser(string)
        # self.assertEqual(r, '??')

        # attribute field has non-null value
        string = r'''_exists_:title'''
        r = query_parser(string)
        self.assertEqual(r, '"attributes"::jsonb ? \'title\'')

    def test_wildcards(self):

        # ? = single character, * = one or more characters
        string = r'''text:qu?ck bro*'''
        r = query_parser(string)
        self.assertEqual(r, '"text" ~* \'qu.?ck bro.*\'')

    def test_regular_expressions(self):

        string = r'''name:/joh?n(ath[oa]n)/'''
        r = query_parser(string)
        self.assertEqual(r, '"name" ~* \'joh?n(ath[oa]n)\'')

    def test_fuzziness(self):
        pass

    def test_proximity_searches(self):
        pass

    # def test_ranges(self):
    #
    #     string = r'''date:[2012-01-01 TO 2012-12-31]'''
    #     r = query_parser(string)
    #     self.assertEqual(r, '??')
    #
    #     string = r'''count:[1 TO 5]'''
    #     r = query_parser(string)
    #     self.assertEqual(r, '??')
    #
    #     string = r'''tag:{alpha TO omega}'''
    #     r = query_parser(string)
    #     self.assertEqual(r, '??')
    #
    #     string = r'''count:[10 TO *]'''
    #     r = query_parser(string)
    #     self.assertEqual(r, '??')
    #
    #     string = r''''date:{* TO 2012-01-01}'''
    #     r = query_parser(string)
    #     self.assertEqual(r, '??')
    #
    #     string = r''''count:[1 TO 5}'''
    #     r = query_parser(string)
    #     self.assertEqual(r, '??')
    #
    # def test_unbounded_ranges(self):
    #
    #     string = r'''age:>10'''
    #     r = query_parser(string)
    #     self.assertEqual(r, '??')
    #
    #     string = r'''age:>=10'''
    #     r = query_parser(string)
    #     self.assertEqual(r, '??')
    #
    #     string = r'''age:<10'''
    #     r = query_parser(string)
    #     self.assertEqual(r, '??')
    #
    #     string = r'''age:<=10'''
    #     r = query_parser(string)
    #     self.assertEqual(r, '??')

    def test_boosting(self):
        pass

    def test_boolean_operators(self):
        pass

    def test_grouping(self):

        # field exact match
        string = r'''(quick OR brown) AND fox'''
        r = query_parser(string)
        self.assertEqual(r, '(("text" ILIKE \'%%quick%%\' OR "text" ILIKE \'%%brown%%\') AND "text" ILIKE \'%%fox%%\')')

        # field exact match
        string = r'''status:(active OR pending) title:(full text search)'''
        r = query_parser(string)
        self.assertEqual(r, '(("status" ILIKE \'%%active%%\' OR "status" ILIKE \'%%pending%%\') OR ("title" ILIKE \'%%full%%\' OR "title" ILIKE \'%%text%%\'))')
