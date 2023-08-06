import requests
import json

class user_info:
	def __init__(self, u):
		self.u = u

	def user_info(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo

	def abbr(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['abbr']

	def clanid(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['clanid']

	def country(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['country']

	def custom_hue(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['custom_hue']

	def favourite_mode(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['favourite_mode']

	def followers_count(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['followers_count']

	def id(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['id']

	def is_online(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['is_online']

	def latest_activity(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['latest_activity']

	def play_style(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['play_style']

	def privileges(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['privileges']

	def registered_on(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['registered_on']

	def username(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['username']

	def username_aka(self):
		r = requests.get(f'https://api.gatari.pw/users/get?u={self.u}').json()
		userinfo = r['users'][0]
		return userinfo['username_aka']


class user_stats:
	def __init__(self, u, mode):
		self.u = u
		self.mode = mode
		
	def user_stats(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats

	def a_count(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['a_count']

	def avg_accuracy(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['avg_accuracy']

	def avg_hits_play(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['avg_hits_play']

	def country_rank(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['country_rank']

	def id(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['id']

	def level(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['level']

	def level_progress(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['level_progress']

	def max_combo(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['max_combo']

	def playcount(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['playcount']

	def playtime(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['playtime']

	def pp(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['pp']

	def rank(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['rank']

	def ranked_score(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['ranked_score']

	def replays_watched(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['replays_watched']

	def s_count(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['s_count']

	def sh_count(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['sh_count']

	def total_hits(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['total_hits']

	def total_score(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['total_score']

	def x_count(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['x_count']

	def xh_count(self):
		r = requests.get(f'https://api.gatari.pw/user/stats?u={self.u}&mode={self.mode}').json()
		userstats = r['stats'] 
		return userstats['xh_count']


class user_recent_scores:
	def __init__(self, u, mode, p, l, f, ppfilter):
		self.u = u
		self.mode = mode
		self.p = p
		self.l = l
		self.f = f
		self.ppfilter = ppfilter

	def beatmap(self):
		beatmaps = []
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['beatmap'])
		return beatmaps

	def beatmaps_ar(self):
		beatmaps = []
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['ar'])
		return beatmaps

	def beatmaps_artist(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['artist'])
		return beatmaps

	def beatmaps_id(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['beatmap_id'])
		return beatmaps

	def beatmap_md5(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['beatmap_md5'])
		return beatmaps

	def beatmapset_id(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['beatmapset_id'])
		return beatmaps

	def beatmap_bpm(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['bpm'])
		return beatmaps

	def beatmap_creator(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['creator'])
		return beatmaps

	def beatmap_difficulty(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['difficulty'])
		return beatmaps

	def beatmap_fc(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['fc'])
		return beatmaps

	def beatmap_hit_lenght(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['hit_lenght'])
		return beatmaps

	def beatmap_od(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['od'])
		return beatmaps

	def beatmap_ranked(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['ranked'])
		return beatmaps

	def beatmap_ranked_status_frozen(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['ranked_status_frozen'])
		return beatmaps

	def beatmap_song_name(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['song_name'])
		return beatmaps

	def beatmap_title(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['title'])
		return beatmaps

	def beatmap_version(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['version'])
		return beatmaps

	def completed(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['completed'])
		return beatmaps

	def count_100(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_100'])
		return beatmaps

	def count_300(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_300'])
		return beatmaps

	def count_50(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_50'])
		return beatmaps

	def count_gekis(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_gekis'])
		return beatmaps

	def count_katu(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_katu'])
		return beatmaps

	def count_miss(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_miss'])
		return beatmaps

	def full_combo(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['full_combo'])
		return beatmaps

	def id(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['id'])
		return beatmaps

	def isfav(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['isfav'])
		return beatmaps

	def max_combo(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['max_combo'])
		return beatmaps

	def mods(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['mods'])
		return beatmaps

	def play_mode(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['play_mode'])
		return beatmaps

	def pp(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['pp'])
		return beatmaps

	def ranking(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['ranking'])
		return beatmaps

	def score(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['score'])
		return beatmaps

	def time(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['time'])
		return beatmaps

	def views(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['views'])
		return beatmaps

	def accuracy(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/recent?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&f={self.f}&ppFilter={self.ppfilter}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['accuracy'])
		return beatmaps

class user_best_scores:
	def __init__(self, u, mode, p, l, mods):
		self.u = u
		self.mode = mode
		self.p = p
		self.l = l
		self.mods = mods

	def accuracy(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['accuracy'])
		return beatmaps

	def beatmap(self):
		beatmaps = []
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['beatmap'])
		return beatmaps

	def beatmaps_ar(self):
		beatmaps = []
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['ar'])
		return beatmaps

	def beatmaps_artist(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['artist'])
		return beatmaps

	def beatmaps_id(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['beatmap_id'])
		return beatmaps

	def beatmap_md5(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['beatmap_md5'])
		return beatmaps

	def beatmapset_id(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['beatmapset_id'])
		return beatmaps

	def beatmap_bpm(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['bpm'])
		return beatmaps

	def beatmap_creator(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['creator'])
		return beatmaps

	def beatmap_difficulty(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['difficulty'])
		return beatmaps

	def beatmap_fc(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['fc'])
		return beatmaps

	def beatmap_hit_lenght(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['hit_lenght'])
		return beatmaps

	def beatmap_od(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['od'])
		return beatmaps

	def beatmap_ranked(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['ranked'])
		return beatmaps

	def beatmap_ranked_status_frozen(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['ranked_status_frozen'])
		return beatmaps

	def beatmap_song_name(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['song_name'])
		return beatmaps

	def beatmap_title(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['title'])
		return beatmaps

	def beatmap_version(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['version'])
		return beatmaps

	def completed(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['completed'])
		return beatmaps

	def count_100(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_100'])
		return beatmaps

	def count_300(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_300'])
		return beatmaps

	def count_50(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_50'])
		return beatmaps

	def count_gekis(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_gekis'])
		return beatmaps

	def count_katu(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_katu'])
		return beatmaps

	def count_miss(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_miss'])
		return beatmaps

	def full_combo(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['full_combo'])
		return beatmaps

	def id(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['id'])
		return beatmaps

	def isfav(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['isfav'])
		return beatmaps

	def max_combo(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['max_combo'])
		return beatmaps

	def mods(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['mods'])
		return beatmaps

	def play_mode(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['play_mode'])
		return beatmaps

	def pp(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['pp'])
		return beatmaps

	def ranking(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['ranking'])
		return beatmaps

	def score(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['score'])
		return beatmaps

	def time(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['time'])
		return beatmaps

	def views(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/best?id={self.u}&l={self.l}&p={self.p}&mode={self.mode}&mods={self.mods}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['views'])
		return beatmaps

class users_first_place:
	def __init__(self, u, mode, p, l):
		self.u = u
		self.mode = mode
		self.p = p
		self.l = l

	def accuracy(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['accuracy'])
		return beatmaps

	def beatmap(self):
		beatmaps = []
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['beatmap'])
		return beatmaps

	def beatmaps_ar(self):
		beatmaps = []
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['ar'])
		return beatmaps

	def beatmaps_artist(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['artist'])
		return beatmaps

	def beatmaps_id(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['beatmap_id'])
		return beatmaps

	def beatmap_md5(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['beatmap_md5'])
		return beatmaps

	def beatmapset_id(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['beatmapset_id'])
		return beatmaps

	def beatmap_bpm(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['bpm'])
		return beatmaps

	def beatmap_creator(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['creator'])
		return beatmaps

	def beatmap_difficulty(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['difficulty'])
		return beatmaps

	def beatmap_fc(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['fc'])
		return beatmaps

	def beatmap_hit_lenght(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['hit_lenght'])
		return beatmaps

	def beatmap_od(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['od'])
		return beatmaps

	def beatmap_ranked(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['ranked'])
		return beatmaps

	def beatmap_ranked_status_frozen(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['ranked_status_frozen'])
		return beatmaps

	def beatmap_song_name(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['song_name'])
		return beatmaps

	def beatmap_title(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['title'])
		return beatmaps

	def beatmap_version(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['version'])
		return beatmaps

	def completed(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['completed'])
		return beatmaps

	def count_100(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_100'])
		return beatmaps

	def count_300(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_300'])
		return beatmaps

	def count_50(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_50'])
		return beatmaps

	def count_gekis(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_gekis'])
		return beatmaps

	def count_katu(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_katu'])
		return beatmaps

	def count_miss(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_miss'])
		return beatmaps

	def full_combo(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['full_combo'])
		return beatmaps

	def id(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['id'])
		return beatmaps

	def isfav(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['isfav'])
		return beatmaps

	def max_combo(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['max_combo'])
		return beatmaps

	def mods(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['mods'])
		return beatmaps

	def play_mode(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['play_mode'])
		return beatmaps

	def pp(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['pp'])
		return beatmaps

	def ranking(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['ranking'])
		return beatmaps

	def score(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['score'])
		return beatmaps

	def time(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['time'])
		return beatmaps

	def views(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/first?id={self.id}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['views'])
		return beatmaps

class uesers_most_played_maps:
	def __init__(self, u, mode, p, l):
		self.u = u
		self.mode = mode
		self.p = p

	def count(self):
		r = requests.get(f'https://api.gatari.pw/user/mostplays?id={self.u}&mode={self.mode}&page={self.p}').json()
		return r['count']

	def beatmaps_id(self):
		r = requests.get(f'https://api.gatari.pw/user/mostplays?id={self.u}&mode={self.mode}&page={self.p}').json()
		beatmaps = []
		for i in range(5):
			beatmap = r['result'][i]
			beatmaps.append(beatmap['beatmap_id'])
		return beatmaps

	def beatmapset_id(self):
		r = requests.get(f'https://api.gatari.pw/user/mostplays?id={self.u}&mode={self.mode}&page={self.p}').json()
		beatmaps = []
		for i in range(5):
			beatmap = r['result'][i]
			beatmaps.append(beatmap['beatmapset_id'])
		return beatmaps

	def creator(self):
		r = requests.get(f'https://api.gatari.pw/user/mostplays?id={self.u}&mode={self.mode}&page={self.p}').json()
		beatmaps = []
		for i in range(5):
			beatmap = r['result'][i]
			beatmaps.append(beatmap['creator'])
		return beatmaps

	def difficulty(self):
		r = requests.get(f'https://api.gatari.pw/user/mostplays?id={self.u}&mode={self.mode}&page={self.p}').json()
		beatmaps = []
		for i in range(5):
			beatmap = r['result'][i]
			beatmaps.append(beatmap['difficulty'])
		return beatmaps

	def playcount(self):
		r = requests.get(f'https://api.gatari.pw/user/mostplays?id={self.u}&mode={self.mode}&page={self.p}').json()
		beatmaps = []
		for i in range(5):
			beatmap = r['result'][i]
			beatmaps.append(beatmap['playcount'])
		return beatmaps

	def song_name(self):
		r = requests.get(f'https://api.gatari.pw/user/mostplays?id={self.u}&mode={self.mode}&page={self.p}').json()
		beatmaps = []
		for i in range(5):
			beatmap = r['result'][i]
			beatmaps.append(beatmap['song_name'])
		return beatmaps

class user_favourite_scores:
	def __init__(self, u, mode, p, l):
		self.u = u
		self.mode = mode
		self.p = p
		self.l = l


	def accuracy(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['accuracy'])
		return beatmaps

	def beatmap(self):
		beatmaps = []
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['beatmap'])
		return beatmaps

	def beatmaps_ar(self):
		beatmaps = []
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['ar'])
		return beatmaps

	def beatmaps_artist(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['artist'])
		return beatmaps

	def beatmaps_id(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['beatmap_id'])
		return beatmaps

	def beatmap_md5(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['beatmap_md5'])
		return beatmaps

	def beatmapset_id(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['beatmapset_id'])
		return beatmaps

	def beatmap_bpm(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['bpm'])
		return beatmaps

	def beatmap_creator(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['creator'])
		return beatmaps

	def beatmap_difficulty(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['difficulty'])
		return beatmaps

	def beatmap_fc(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['fc'])
		return beatmaps

	def beatmap_hit_lenght(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['hit_lenght'])
		return beatmaps

	def beatmap_od(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['od'])
		return beatmaps

	def beatmap_ranked(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['ranked'])
		return beatmaps

	def beatmap_ranked_status_frozen(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['ranked_status_frozen'])
		return beatmaps

	def beatmap_song_name(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['song_name'])
		return beatmaps

	def beatmap_title(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['title'])
		return beatmaps

	def beatmap_version(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmap = beatmap['beatmap']
			beatmaps.append(beatmap['version'])
		return beatmaps

	def completed(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['completed'])
		return beatmaps

	def count_100(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_100'])
		return beatmaps

	def count_300(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_300'])
		return beatmaps

	def count_50(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_50'])
		return beatmaps

	def count_gekis(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_gekis'])
		return beatmaps

	def count_katu(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_katu'])
		return beatmaps

	def count_miss(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['count_miss'])
		return beatmaps

	def full_combo(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['full_combo'])
		return beatmaps

	def id(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['id'])
		return beatmaps

	def isfav(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['isfav'])
		return beatmaps

	def max_combo(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['max_combo'])
		return beatmaps

	def mods(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['mods'])
		return beatmaps

	def play_mode(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['play_mode'])
		return beatmaps

	def pp(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['pp'])
		return beatmaps

	def ranking(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['ranking'])
		return beatmaps

	def score(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['score'])
		return beatmaps

	def time(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['time'])
		return beatmaps

	def views(self):
		r = requests.get(f'https://api.gatari.pw/user/scores/favs?id={self.u}&mode={self.mode}&p={self.p}&l={self.l}').json()
		for i in range(self.l):
			beatmap = r['scores'][i]
			beatmaps.append(beatmap['views'])
		return beatmaps


