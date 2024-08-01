from repository.meme_repository import MemeRepo


class MemeService:
    def __init__(self, meme_repo: "MemeRepo"):
        self.meme_repo = meme_repo
    