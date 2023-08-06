import numpy as np
import pandas as pd
from .raw_data_helper import RawDataHelper
from ...view.raw_models import OSFundInfo, OSFundNav, OSFundBenchmark

class OtherRawDataDownloader:

    def __init__(self, data_helper):
        self._data_helper = data_helper

    def oversea_fund_info(self, fund_info):
        fund_info_dic = {
            '基金id':'codes',
            '基金名称':'desc_name',
            '基金管理公司':'company_name',
            '基金类型':'fund_type',
            '行业':'industry',
            '地区':'area',
            '最新净值':'latest_nav',
            '基金系列':'fund_series',
            '是否为新基金':'is_new_fund',
            '赎回资金到账天数':'redeem_dates',
            '换出基金指示滞延时间':'excg_out_t_delay',
            '换入基金指示滞延时间':'excg_in_t_delay',
            '最低初始投资额':'min_init_trade_amt',
            '最低后续投资额':'min_ag_trade_amt',
            '最小赎回类型':'min_redeem_type',
            '最小赎回数量':'min_redeem_vol',
            '最小持有类型':'min_pos_type',
            '最小持有数量':'min_pos_vol',
            '申购周期':'purchase_period',
            '风险级别':'risk_level',
            '可供认购':'is_purchase',
            '证监会是否认可':'is_CSRC_approve',
            '年费':'yearly_fee',
            '申购处理频率':'purchase_process_freq',
            '币种':'money_type',
            '支持转换基金':'is_sup_exchg_fund',
            '支持转换为同系列其他基金':'is_sup_same_series_fund',
            '支持同系列其他基金转换为本基金':'is_sup_same_series_exchg',
            '赎回费(%)':'redeem_fee',
            '赎回方式':'redeem_method',
            '是否衍生产品':'is_derivatives',
            '股息分派方式':'divident_distbt_mtd',
            '派息频率':'divident_freq',
            '资产类别':'asset_type',
            '资产编号':'asset_code',
            '发行日期':'issue_date',
            '发行价':'issue_price',
            '基金规模（单位：百万）':'fund_size_biln',
            '基金规模统计日期':'fund_size_calc_date',
            '基金规模币种':'fund_size_money_type',
            '费率':'fee_rate',
            '费率统计日期':'fee_calc_date',
            '复杂产品':'is_compx_product',
        }
        delete_cols = ['发布日期','处理结果']
        date_list = ['发行日期','费率统计日期','基金规模统计日期']
        con_list = ['是否为新基金','可供认购','证监会是否认可','支持转换基金','支持转换为同系列其他基金',
                '是否衍生产品','复杂产品','支持同系列其他基金转换为本基金']

        for date_col in date_list:
            td = pd.to_datetime(fund_info[date_col])
            td = [i.date() for i in td]
            fund_info.loc[:,date_col] = td

        for del_col in delete_cols:
            fund_info = fund_info.drop(columns=[del_col])

        for con_col in con_list:
            fund_info.loc[:,con_col] = fund_info[con_col].replace({'是':True, '否':False,})
            
        fund_info = fund_info.rename(columns=fund_info_dic)
        self._data_helper._upload_raw(fund_info, OSFundInfo.__table__.name)

    def oversea_fund_nav(self, df):
        td = pd.to_datetime(df.datetime)
        td = [i.date() for i in td]
        df['datetime'] = td
        self._data_helper._upload_raw(df, OSFundNav.__table__.name)

    def oversea_fund_benchmark(self, df):
        dic = {
            '#N/A Field Not Applicable':None,
            '#N/A Invalid Security':None,
        }
        df = df.replace(dic)
        self._data_helper._upload_raw(df, OSFundBenchmark.__table__.name)