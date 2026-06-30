from app.data.dataset_loader import DatasetLoader
from app.data.dataset_search import DatasetSearch
from app.core.planner import Planner

loader = DatasetLoader("datasets")
loader.load_datasets()

search = DatasetSearch(loader)

planner = Planner(search)