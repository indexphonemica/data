import unittest
import commit
import iphon_configparser
import configparser # needed for getting the errors

# TODO: 
# - test phoneme dups where one is marginal/loan and one isn't
# - reject if there are multiple >s
# - invalid phonemes tests
# - actually test glottolog bibkeys, ideally with pyglottolog

def v(str):
	c = iphon_configparser.parser()
	c.read_string(string=str)
	return commit.validate(c)

class CoreTest(unittest.TestCase):
	def test_sections(self):
		with self.assertRaises(commit.IncorrectSectionsError):
			v("""[core]
				name = Test
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[phonotactics]
				no_info

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")

	def test_core_name(self):
		with self.assertRaises(commit.MissingPropertyError):
			v("""[core]
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				no_info

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")

	def test_core_glottocode(self):
		with self.assertRaises(commit.MissingPropertyError):
			v("""[core]
				name = Test

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				no_info

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")

	def test_core_name_required(self):
		with self.assertRaises(commit.MissingPropertyError):
			v("""[core]
				name = REQUIRED
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				no_info

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")

	def test_core_glottocode_required(self):
		with self.assertRaises(commit.MissingPropertyError):
			v("""[core]
				name = Test
				glottocode = REQUIRED

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				no_info

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")

	def test_core_null_name(self):
		with self.assertRaises(commit.MissingPropertyError):
			v("""[core]
				name
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				no_info

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")

	def test_core_null_glottocode(self):
		with self.assertRaises(commit.MissingPropertyError):
			v("""[core]
				name = Test
				glottocode

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				no_info

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")

	def test_core_blank_name(self):
		with self.assertRaises(commit.MissingPropertyError):
			v("""[core]
				name =   
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				no_info

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")

class SourceTest(unittest.TestCase):
	def test_no_glottolog_no_author(self):
		with self.assertRaises(commit.MissingPropertyError):
			v("""[core]
				name = Test
				glottocode = test1234

				[source]
				title = Test
				year = 2019
				url = http://example.com/

				[notes]

				[phonotactics]
				no_info

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")

	def test_author_name_formatting(self):
		with self.assertRaises(commit.InvalidPropertyError):
			v("""[core]
				name = Test
				glottocode = test1234

				[source]
				author = John Smith
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				no_info

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")

	def test_invalid_glottolog(self):
		pass # TODO?

class PhonemesTest(unittest.TestCase):
	def test_no_phonemes(self):
		with self.assertRaises(commit.IncorrectSectionsError):
			v("""[core]
				name = Test
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]
				This is a note.

				[phonotactics]
				no_info

				[phonemes]

				[allophonic_rules]
				""")

	def test_phonemes_required(self):
		with self.assertRaises(commit.IncorrectSectionsError):
			v("""[core]
				name = Test
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				no_info

				[phonemes]
				REQUIRED

				[allophonic_rules]
				""")

	def test_no_duplicate_phonemes(self):
		with self.assertRaises(configparser.DuplicateOptionError):
			v("""[core]
				name = Test
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				no_info

				[phonemes]
				p
				t
				k
				p
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")

	# commented out for now since we don't have 100% phonotactics coverage yet (TODO)
	# def test_phonotactics_required(self):
	# 	with self.assertRaises(commit.IncorrectSectionsError):
	# 		v("""[core]
	# 			name = Test
	# 			glottocode = test1234

	# 			[source]
	# 			glottolog = 1234
	# 			url = http://example.com/

	# 			[notes]

	# 			[phonotactics]
	# 			no_info

	# 			[phonemes]
	# 			p
	# 			t
	# 			k
	# 			a
	# 			i
	# 			u

	# 			[allophonic_rules]
	# 			p > b / V_V
	# 			t > s ~ ts / _i
	# 			u >~ o / _""")

	def test_phonotactics_sanity_check(self):
		with self.assertRaises(commit.InvalidPropertyError):
			v("""
				[core]
				name = Test
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				max_initial = 0
				max_final = 21

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")

	def test_phonotactics_max_initial_and_final_required_if_no_info_not_present(self):
		with self.assertRaises(commit.MissingPropertyError):
			v("""
				[core]
				name = Test
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")
		with self.assertRaises(commit.MissingPropertyError):
			v("""
				[core]
				name = Test
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				max_initial = 1

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")
		with self.assertRaises(commit.MissingPropertyError):
			v("""
				[core]
				name = Test
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

				[phonotactics]
				max_initial = 1
				max_final

				[phonemes]
				p
				t
				k
				a
				i
				u

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				u >~ o / _""")


class CorrectTest(unittest.TestCase):
	def test_passes_correct(self):
		self.assertEqual(
			v("""[core]
				name = Test
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]
				Here is a note.

				[phonotactics]
				no_info

				[phonemes]
				p
				t
				k
				a
				i
				u|o
				(f)

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				t > ɾ
				f > h / _a
				a+i >~ e"""), True)
		self.assertEqual(
			v("""[core]
				name = Test
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]
				Here is a note.

				[phonotactics]
				max_initial = 2
				max_final = 1

				[phonemes]
				p
				t
				k
				a
				i
				u|o
				(f)

				[allophonic_rules]
				p > b / V_V
				t > s ~ ts / _i
				t > ɾ
				f > h / _a
				a+i >~ e"""), True)

if __name__ == '__main__':
	unittest.main()