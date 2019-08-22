import unittest
import commit
import configparser

def v(str):
	c = configparser.ConfigParser(allow_no_value=True)
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
		# TODO - we'll need to change all the existing test glottolog bibkeys too
		pass

class PhonemesTest(unittest.TestCase):
	def test_no_phonemes(self):
		with self.assertRaises(commit.MissingPropertyError):
			v("""[core]
				name = Test
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]
				This is a note.

				[phonemes]

				[allophonic_rules]
				""")

	def test_phonemes_REQUIRED(self):
		with self.assertRaises(commit.MissingPropertyError):
			v("""[core]
				name = Test
				glottocode = test1234

				[source]
				glottolog = 1234
				url = http://example.com/

				[notes]

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
	# TODO: invalid phonemes tests



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