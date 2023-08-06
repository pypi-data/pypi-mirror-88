from .compute_fund_daily_collection import FundDailyCollectionProcessor
from .compute_index_daily_collection import IndexDailyCollectionProcessor
from .compute_aic_daily_collection import AICDailyCollectionProcessor
from .compute_stock_ipo_collection import StockIpoCollectionProcessor, ConvBondIpoCollection

class ViewDataProcessor(object):
    def __init__(self):
        self.fund_daily_collection_processor = FundDailyCollectionProcessor()
        self.index_daily_collection_processor = IndexDailyCollectionProcessor()
        self.aic_daily_collection_processor = AICDailyCollectionProcessor()
        self.stock_ipo_collection = StockIpoCollectionProcessor()
        self.conv_bond_ipo_collection = ConvBondIpoCollection()

    def process_all(self, start_date, end_date):
        failed_tasks = []

        failed_tasks.extend(self.fund_daily_collection_processor.process())
        failed_tasks.extend(self.index_daily_collection_processor.process())
        failed_tasks.extend(self.aic_daily_collection_processor.process())
        failed_tasks.extend(self.stock_ipo_collection.process())
        failed_tasks.extend(self.conv_bond_ipo_collection.process())
        return failed_tasks
