from os.path import join, dirname

from audiobooker.scrappers.audioanarchy import AudioAnarchy
from ovos_utils.parse import fuzzy_match, MatchStrategy
from ovos_utils.ocp import MediaType, PlaybackType
from ovos_workshop.decorators.ocp import ocp_search, ocp_featured_media
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill



class AudioAnarchySkill(OVOSCommonPlaybackSkill):
    def __init__(self, *args, **kwargs):
        self.supported_media = [MediaType.GENERIC, MediaType.AUDIOBOOK]
        self.skill_icon = join(dirname(__file__), "ui", "logo.gif")
        self.skill_bg = join(dirname(__file__), "ui", "bg.png")
        super().__init__(*args, **kwargs)

    def calc_score(self, phrase, match, idx=0, base_score=0):
        # idx represents the order from librivox
        score = base_score - idx  # - 1% as we go down the results list

        score += 100 * fuzzy_match(phrase.lower(), match.title.lower(),
                                   strategy=MatchStrategy.TOKEN_SET_RATIO)

        return min(100, score)

    # common play
    @ocp_search()
    def search_audio_anarchy_audiobooks(self, phrase, media_type):
        # match the request media_type
        base_score = 0
        if media_type == MediaType.AUDIOBOOK:
            base_score += 25
        else:
            base_score -= 15

        if self.voc_match(phrase, "audioanarchy"):
            # explicitly requested audioanarchy
            base_score += 60
            phrase = self.remove_voc(phrase, "audioanarchy")

        loyalbooks = AudioAnarchy()

        results = loyalbooks.search_audiobooks(title=phrase)
        for idx, book in enumerate(results):
            score = self.calc_score(phrase, book, idx=idx,
                                    base_score=base_score)
            yield self._book2ocp(book, score)

    @ocp_featured_media()
    def featured_media(self):
        for book in AudioAnarchy().scrap_popular():
            yield self._book2ocp(book)

    def _book2ocp(self, book, score=50):
        author = " ".join([au.first_name + au.last_name for au in
                           book.authors])
        pl = [{
            "match_confidence": score,
            "media_type": MediaType.AUDIOBOOK,
            "uri": s,
            "artist": author,
            "playback": PlaybackType.AUDIO,
            "image": book.img,
            "bg_image": book.img,
            "skill_icon": self.skill_icon,
            "title": s.split("/")[-1].split(".")[0].replace("_", " "),
            "skill_id": self.skill_id
        } for ch, s in enumerate(book.streams)]

        return {
            "match_confidence": score,
            "media_type": MediaType.AUDIOBOOK,
            "playback": PlaybackType.AUDIO,
            "playlist": pl,  # return full playlist result
            "length": book.runtime * 1000,
            "image": book.img,
            "artist": author,
            "bg_image": book.img,
            "skill_icon": self.skill_icon,
            "title": book.title,
            "skill_id": self.skill_id
        }

