from yahooquery import search
def name_to_ticker(user_in):
    """
    searches for companies matching the user's input
    parameters:user_in str
    returns:
        list:top 5 equity search results
    """
    search_results=search(user_in)
    op_search_results=[]
    count=0
    #selecting top 5 equity type only search results
    for i in search_results["quotes"]:
        if i["quoteType"]=="EQUITY" and count<5:
            op_search_results.append(i)
            count+=1
    return(op_search_results)
    #tickers are extracted in app.py
# #testing
# a=name_to_ticker("apple")
# print(a)

# for result in a:
#     print(result["shortname"], "(", result["symbol"], ")")