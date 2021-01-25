#--- IMPORTS
import json
import os
import requests
import shutil as sh
import sys

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

#--- CONFIG VARS
PACK_NAME = "EmojiChat"
PACK_DESCRIPTION = "Default EmojiChat pack."
PACK_VERSION = "1.0.0"
SHEET_WIDTH = 256
EMOJI_WIDTH = 16
EMOJI_REPO_URL = "https://api.github.com/repos/twitter/twemoji/releases/latest"
EMOJI_DISCORD_JSON_URL = "https://raw.githubusercontent.com/amethyst-studio/discord-emoji/main/_snapshot.json"
with open('./config.json', encoding="utf8") as f:
	data = json.load(f)
	PACK_DESCRIPTION = data['PACK_DESCRIPTION']
	PACK_VERSION = data['PACK_VERSION']
	SHEET_WIDTH = data['SHEET_WIDTH']
	EMOJI_WIDTH = data['EMOJI_WIDTH']
	EMOJI_REPO_URL = data['EMOJI_REPO_URL']
	EMOJI_DISCORD_JSON_URL = data['EMOJI_DISCORD_JSON_URL']
	PACK_NAME = data['PACK_NAME']
if not (SHEET_WIDTH / EMOJI_WIDTH).is_integer():
	exit("Bad sheet or emoji width. sheet/emoji should give an integer")

#--- VARS
CACHE_DIR = './cache'
EMOJI_JSON_NAME = '_snapshot.json'
EMOJI_JSON_DIR = CACHE_DIR + '/' + EMOJI_JSON_NAME
FILENAME_JSON = './temp/filenames.json'
FILENAME_JSON_CUSTOM = './temp/filenames_custom.json'
IMAGE_DIR = './cache/images'
SPECIAL_EMOJIS = ['relaxed', 'frowning2', 'white_frowning_face', 'skull_crossbones', 'skull_and_crossbones', 'v', 'point_up', 'hand_splayed', 'raised_hand_with_fingers_splayed', 'writing_hand', 'eye', 'speaking_head', 'speaking_head_in_silhouette', 'detective', 'spy', 'sleuth_or_spy', 'levitate', 'man_in_business_suit_levitating', 'helmet_with_cross', 'helmet_with_white_cross', 'dark_sunglasses', 'spider', 'spider_web', 'dove', 'dove_of_peace', 'chipmunk', 'shamrock', 'comet', 'cloud_tornado', 'cloud_with_tornado', 'sunny', 'white_sun_small_cloud', 'white_sun_with_small_cloud', 'white_sun_cloud', 'white_sun_behind_cloud', 'cloud', 'white_sun_rain_cloud', 'white_sun_behind_cloud_with_rain', 'cloud_rain', 'cloud_with_rain', 'thunder_cloud_rain', 'thunder_cloud_and_rain', 'cloud_lightning', 'cloud_with_lightning', 'cloud_snow', 'cloud_with_snow', 'snowflake', 'snowman2', 'wind_blowing_face', 'umbrella2', 'fog', 'hot_pepper', 'fork_knife_plate', 'fork_and_knife_with_plate', 'ice_skate', 'skier', 'person_lifting_weights', 'lifter', 'weight_lifter', 'person_bouncing_ball', 'basketball_player', 'person_with_ball', 'person_golfing', 'golfer', 'military_medal', 'rosette', 'reminder_ribbon', 'tickets', 'admission_tickets', 'chess_pawn', 'race_car', 'racing_car', 'motorcycle', 'racing_motorcycle', 'airplane', 'airplane_small', 'small_airplane', 'satellite_orbital', 'motorboat', 'cruise_ship', 'passenger_ship', 'ferry', 'map', 'world_map', 'stadium', 'beach_umbrella', 'umbrella_on_ground', 'beach', 'beach_with_umbrella', 'island', 'desert_island', 'desert', 'mountain', 'mountain_snow', 'snow_capped_mountain', 'camping', 'homes', 'house_buildings', 'house_abandoned', 'derelict_house_building', 'construction_site', 'building_construction', 'classical_building', 'shinto_shrine', 'railway_track', 'railroad_track', 'motorway', 'park', 'national_park', 'cityscape', 'keyboard', 'desktop', 'desktop_computer', 'printer', 'mouse_three_button', 'three_button_mouse', 'trackball', 'joystick', 'compression', 'projector', 'film_projector', 'film_frames', 'telephone', 'microphone2', 'studio_microphone', 'level_slider', 'control_knobs', 'stopwatch', 'timer', 'timer_clock', 'clock', 'mantlepiece_clock', 'candle', 'oil', 'oil_drum', 'scales', 'hammer_pick', 'hammer_and_pick', 'tools', 'hammer_and_wrench', 'pick', 'gear', 'chains', 'dagger', 'dagger_knife', 'crossed_swords', 'shield', 'coffin', 'urn', 'funeral_urn', 'alembic', 'hole', 'thermometer', 'bellhop', 'bellhop_bell', 'key2', 'old_key', 'couch', 'couch_and_lamp', 'bed', 'frame_photo', 'frame_with_picture', 'shopping_bags', 'envelope', 'label', 'notepad_spiral', 'spiral_note_pad', 'calendar_spiral', 'spiral_calendar_pad', 'wastebasket', 'card_box', 'card_file_box', 'ballot_box', 'ballot_box_with_ballot', 'file_cabinet', 'dividers', 'card_index_dividers', 'newspaper2', 'rolled_up_newspaper', 'paperclips', 'linked_paperclips', 'scissors', 'pen_ballpoint', 'lower_left_ballpoint_pen', 'pen_fountain', 'lower_left_fountain_pen', 'black_nib', 'paintbrush', 'lower_left_paintbrush', 'crayon', 'lower_left_crayon', 'pencil2', 'heart', 'heart_exclamation', 'heavy_heart_exclamation_mark_ornament', 'peace', 'peace_symbol', 'cross', 'latin_cross', 'star_and_crescent', 'om_symbol', 'wheel_of_dharma', 'star_of_david', 'yin_yang', 'orthodox_cross', 'atom', 'atom_symbol', 'radioactive', 'radioactive_sign', 'biohazard', 'biohazard_sign', 'u6708', 'eight_pointed_black_star', 'secret', 'congratulations', 'a', 'b', 'o2', 'hotsprings', 'bangbang', 'interrobang', 'part_alternation_mark', 'warning', 'fleur_de_lis', 'recycle', 'sparkle', 'eight_spoked_asterisk', 'm', 'parking', 'sa', 'information_source', 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'hash', 'asterisk', 'keycap_asterisk', 'eject', 'eject_symbol', 'arrow_forward', 'pause_button', 'double_vertical_bar', 'play_pause', 'stop_button', 'record_button', 'track_next', 'next_track', 'track_previous', 'previous_track', 'arrow_backward', 'arrow_right', 'arrow_left', 'arrow_up', 'arrow_down', 'arrow_upper_right', 'arrow_lower_right', 'arrow_lower_left', 'arrow_upper_left', 'arrow_up_down', 'left_right_arrow', 'arrow_right_hook', 'leftwards_arrow_with_hook', 'arrow_heading_up', 'arrow_heading_down', 'heavy_multiplication_x', 'infinity', 'tm', 'copyright', 'registered', 'wavy_dash', 'heavy_check_mark', 'ballot_box_with_check', 'black_small_square', 'white_small_square', 'black_medium_square', 'white_medium_square', 'speech_left', 'left_speech_bubble', 'anger_right', 'right_anger_bubble', 'spades', 'clubs', 'hearts', 'diamonds', 'female_sign', 'male_sign', 'medical_symbol', 'flag_white']
CUSTOM_EMOJIS = './assets/custom_emojis'
CACHE_ZIP_DIR = './cache/zips/'
CACHE_IMGS_DIR = './cache/images/'
TEMP_UNZIPPED_DIR = './temp/unzipped/'
PRODUCTION_DIR = './production'

#--- FUNCTIONS
def get_emoji_json_data():
	with open(EMOJI_JSON_DIR, encoding="utf8") as f:
		return json.load(f)

def get_filename_json_data():
	with open(FILENAME_JSON) as f:
		return json.load(f)

def get_filename_json_custom_data():
	with open(FILENAME_JSON_CUSTOM) as f:
		return json.load(f)

def uncategorize_emoji_json():
	data = get_emoji_json_data()
	new_data = {}
	people_key_found = False
	for key in data:
		if key == 'people':
			people_key_found = True
			break
	if people_key_found:
		for key in data:
			for subkey in data[key]:
				new_data[subkey] = data[key][subkey]
		with open(EMOJI_JSON, 'w', encoding="utf8") as f:
			f.seek(0)
			json.dump(new_data, f, indent=4)
			f.truncate()

def get_image_name_from_unicode(unicode_str, dict_key):
	string = []
	for char in unicode_str:
		a = hex(ord(char))
		if not (a == '0xfe0f' and dict_key in SPECIAL_EMOJIS):
			string.append(a[2:])
	return '-'.join(string) + '.png'

def get_name_from_utf(name):
	print(hex(ord(name)))

def gen_name_filename_json():
	print('Generating temp emoji jsons')
	#Stock emojis
	Path('./temp').mkdir(parents=True, exist_ok=True)
	data = get_emoji_json_data()
	new_data = {}
	for key in data:
		for subkey in data[key]:
			new_data[subkey] = IMAGE_DIR + '/' + get_image_name_from_unicode(data[key][subkey], subkey)
	folder = os.listdir(CUSTOM_EMOJIS)
	for picture in folder:
		new_data[picture[:picture.rfind('.')]] = CUSTOM_EMOJIS + '/' + picture
	with open(FILENAME_JSON, 'w', encoding="utf8") as f:
		f.seek(0)
		json.dump(new_data, f, indent=4)
		f.truncate()

	#Custom emojis
	new_data = {}
	for picture in folder:
		new_data[picture[:picture.rfind('.')]] = CUSTOM_EMOJIS + '/' + picture
	with open(FILENAME_JSON_CUSTOM, 'w', encoding="utf8") as f:
		f.seek(0)
		json.dump(new_data, f, indent=4)
		f.truncate()

def check_images():
	print('Checking for differences between ' + EMOJI_JSON_NAME + ' and the emoji images')
	folder = os.listdir(IMAGE_DIR)
	folder_custom = os.listdir(CUSTOM_EMOJIS)
	image_data = get_filename_json_data()
	missing = []
	for key in image_data:
		#print(image_data[key][image_data[key].rfind('/') + 1:])
		if not (image_data[key][image_data[key].rfind('/') + 1:] in folder or image_data[key][image_data[key].rfind('/') + 1:] in folder_custom):
			missing.append(key)
			print('Missing image for ' + key)
	print("', '".join(missing))
	if len(missing) > 0:
		exit()
	print('All good')

def create_lists():
	print("Generating emoji lists")
	Path('./temp').mkdir(parents=True, exist_ok=True)
	file_data = get_filename_json_data()
	#print(len(file_data.keys()))
	with open('./production/emoji_list.txt', 'w') as f:
		for key in file_data:
			f.write('%s\n' % key)
	with open('./production/server_emojis.txt', 'w') as f:
		folder = os.listdir(CUSTOM_EMOJIS)
		for file in folder:
			f.write("%s\n" % file[:file.rfind('.')])
	with open('./production/emoji_aliases.txt', 'w') as f:
		f.write('Put emoji aliases here, one at each line, corresponding to alphabetical order of image files')
	with open('./production/server_emoji_ids.txt', 'w') as f:
		f.write('Put emoji ids here, one at each line, corresponding to alphabetical order of image files')
	#with open('./production/emoji_list_colons.txt', 'w') as f:
	#	for key in file_data:
	#		f.write(':' +key + ':\n')

#emoji_size EMOJI_WIDTHxEMOJI_WIDTH
def create_texture_pack():
	print("Generating resourcepack")
	dir_list = ['./temp/assets/minecraft/font', './temp/assets/minecraft/textures/font']
	for path in dir_list:
		Path(path).mkdir(parents=True, exist_ok=True)
	try:
		sh.copyfile('./assets/texture_pack_files/pack.png', './temp/pack.png')
	except Exception as e:
		print("WARINING: No texture pack logo found")
	try:
		sh.copyfile('./assets/texture_pack_files/default.json', './temp/assets/minecraft/font/default.json')
	except Exception as e:
		exit("ERROR: no file 'default.json' found. Download it again")
	try:
		sh.copyfile('./assets/texture_pack_files/glyph_sizes.bin', './temp/assets/minecraft/font/glyph_sizes.bin')
	except Exception as e:
		exit("ERROR: no file 'glyph_sizes.bin' found. Download it again")
	mcmeta = {"pack": {"pack_format": 4,"description": PACK_DESCRIPTION + ' ' + PACK_VERSION}}
	with open('./temp/pack.mcmeta', 'w', encoding="utf8") as f:
		f.seek(0)
		json.dump(mcmeta, f, indent=4)
		f.truncate()
	file_data = get_filename_json_data()
	current_image = Image.new("RGBA", (SHEET_WIDTH, SHEET_WIDTH))
	counter = 0
	counter_y = 0
	iteration = 0
	starting_char = 172
	emote = 0
	for key in file_data:
		temp_img = Image.open(file_data[key])
		#print(str(emote) + ": " + key)
		emote += 1
		temp_img = temp_img.resize((EMOJI_WIDTH, EMOJI_WIDTH), Image.ANTIALIAS)
		current_image.paste(temp_img, ((counter * EMOJI_WIDTH) % SHEET_WIDTH, counter_y * EMOJI_WIDTH))
		counter += 1
		if (counter * EMOJI_WIDTH) % SHEET_WIDTH == 0:
			counter_y += 1
		if counter >= SHEET_WIDTH / EMOJI_WIDTH * SHEET_WIDTH / EMOJI_WIDTH:
			counter = 0
			counter_y = 0
			#print("=============")
			print("saving unicode_page_" + hex(starting_char + iteration)[2:] + ".png")
			#print("=============")
			current_image.save("./temp/assets/minecraft/textures/font/unicode_page_" + hex(starting_char + iteration)[2:] + ".png", "PNG")
			iteration += 1
			current_image = Image.new("RGBA", (SHEET_WIDTH, SHEET_WIDTH))
	if counter != 0 or counter_y != 0:
		current_image.save("./temp/assets/minecraft/textures/font/unicode_page_" + hex(starting_char + iteration)[2:] + ".png", "PNG")
	os.remove(FILENAME_JSON)
	os.remove(FILENAME_JSON_CUSTOM)
	print('Generating resourcepack zip: ' + PRODUCTION_DIR + '/' + PACK_NAME + PACK_VERSION + '.zip')
	sh.make_archive(PRODUCTION_DIR + '/' + PACK_NAME + PACK_VERSION, 'zip', './temp')
	sh.rmtree('./temp')

def check_for_update():
	print('Checking for emoji sheet update')
	Path(CACHE_ZIP_DIR).mkdir(parents=True, exist_ok=True)
	if len(os.listdir(CACHE_ZIP_DIR)) == 0:
		print('Cache empty')
		return True
	response = requests.get(EMOJI_REPO_URL)
	folder = os.listdir(CACHE_ZIP_DIR)
	for file in folder:
		if response.json()['tag_name'] in file:
			return False
	print('Update found')
	return True

def download_emojis():
	print("Downloading latest emojis...")
	sh.rmtree(CACHE_ZIP_DIR)
	Path(CACHE_ZIP_DIR).mkdir(parents=True, exist_ok=True)
	response = requests.get(EMOJI_REPO_URL)
	url = response.json()['zipball_url']
	r = requests.get(url, allow_redirects=True)
	open(CACHE_ZIP_DIR + response.json()['tag_name'] + '.zip', 'wb').write(r.content)

def handle_unzip():
	print('Unzipping emojis and moving')
	Path(CACHE_IMGS_DIR).mkdir(parents=True, exist_ok=True)
	if len(os.listdir(CACHE_ZIP_DIR)) != 0:
		sh.rmtree(CACHE_IMGS_DIR)
	Path(CACHE_IMGS_DIR).mkdir(parents=True, exist_ok=True)
	Path(CACHE_IMGS_DIR).mkdir(parents=True, exist_ok=True)
	sh.unpack_archive(CACHE_ZIP_DIR + os.listdir(CACHE_ZIP_DIR)[0], extract_dir=TEMP_UNZIPPED_DIR, format='zip')
	folder = os.listdir(TEMP_UNZIPPED_DIR + os.listdir(TEMP_UNZIPPED_DIR)[0] + '/assets/72x72')
	for p in folder:
		sh.move(TEMP_UNZIPPED_DIR + os.listdir(TEMP_UNZIPPED_DIR)[0] + '/assets/72x72/' + p, CACHE_IMGS_DIR + p)
	sh.rmtree(TEMP_UNZIPPED_DIR)

def download_snapshot_json():
	print('Downloading ' + EMOJI_JSON_NAME + '...')
	r = requests.get(EMOJI_DISCORD_JSON_URL, allow_redirects=True)
	open(EMOJI_JSON_DIR, 'wb').write(r.content)

def handle_emoji_dl():
	if check_for_update():
		download_emojis()
		handle_unzip()
		download_snapshot_json()

handle_emoji_dl()


gen_name_filename_json()
check_images()
create_lists()
create_texture_pack()