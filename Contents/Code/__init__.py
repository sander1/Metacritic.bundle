API_URL = 'https://byroredux-metacritic.p.mashape.com/search/movie'

####################################################################################################
def Start():

	HTTP.Headers['User-Agent'] = 'Plex Media Server/0.9'
	HTTP.Headers['X-Mashape-Key'] = '7o60PGcAVLmshjnGCFnhgZnkmFHlp1KDMMHjsn8ROsKmhryyFT'

####################################################################################################
class Metacritic(Agent.Movies):

	name = 'Metacritic'
	languages = [Locale.Language.NoLanguage]
	primary_provider = False
	contributes_to = [
		'com.plexapp.agents.imdb',
		'com.plexapp.agents.themoviedb'
	]

	def search(self, results, media, lang):

		results.Append(MetadataSearchResult(
			id = '%s|%s' % (media.primary_metadata.title, media.primary_metadata.year),
			score = 100
		))

	def update(self, metadata, media, lang):

		(title, year) = metadata.id.rsplit('|', 1)

		# If we already have a Metacritic rating and this is a slightly older movie, do not
		# re-retrieve the rating, lowering the number of API calls.
		if metadata.rating and int(year) < (Datetime.Now().year - 2):
			Log('*** Already got a Metacritic rating for "%s": %s ***' % (title, metadata.rating))
			return None

		post_values = {
			'max_pages': '1',
			'retry': '4',
			'title': title,
			'year_from': year,
			'year_to': str(int(year) + 1) if year != '' else ''
		}

		try:
			json_obj = JSON.ObjectFromURL(API_URL, values=post_values)
		except:
			Log('*** Error retrieving data for "%s" ***' % (title))
			return None

		if 'results' in json_obj and len(json_obj['results']) > 0:
			metadata.rating = float(json_obj['results'][0]['score'])/10
