# Google trend exploration automation
# Timothy Price @ blog.idigitalfuture.com
# github.com/idigitalfuture/Blog/blob/master/trend_research/auto_trend/
# July 2020

from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq(hl='en-US', tz=570)

# recursive function to add all related keywords and associated trends to dataframe
def add_to_list(keywords, depth, threshold, counter=0):

    print('depth: {}'.format(counter))
    # initialize DataFrame
    trend_terms = pd.DataFrame()

    for keyword in keywords:
        print(keyword)

        # create list of related terms and add to top-parent DataFrame
        pytrends.build_payload([keyword], cat=0, timeframe='today 3-m', geo='US', gprop='')
        init_queries = pytrends.related_queries()[keyword]['rising']

        if init_queries is not None:
            init_queries_top = init_queries[init_queries.value > threshold]
            print("init_queries top: {}".format(init_queries_top))
            trend_terms = trend_terms.append(init_queries_top,  ignore_index=True)

            if counter < depth and init_queries_top is not None:
                # find terms related to all items in list
                trend_terms = trend_terms.append(add_to_list(init_queries_top['query'].tolist(), depth, threshold, counter+1), ignore_index=True)

    return trend_terms.drop_duplicates(subset='query', keep='first').sort_values(by=['value'], ascending=False)
