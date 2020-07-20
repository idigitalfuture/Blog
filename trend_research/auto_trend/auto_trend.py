# Google trend exploration automation
# Timothy Price @ blog.idigitalfuture.com
# July 2020

from pytrends.request import TrendReq
import pandas as pd

THRESHOLD = 350

pytrends = TrendReq(hl='en-US', tz=570)

init_keyword = ["Blockchain"]

# recursive function to add all related keywords and associated trends to dataframe
def add_to_list(keywords, count, threshold, counter=0):

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

            if counter < count and init_queries_top is not None:
                # find terms related to all items in list
                trend_terms = trend_terms.append(add_to_list(init_queries_top['query'].tolist(), count, threshold, counter+1), ignore_index=True)

    return trend_terms.drop_duplicates(subset='query', keep='first')
