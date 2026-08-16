from yahooquery import search
def name_to_ticker(user_in):
    """
    converts the input entered to a list of companies and returns the chosen ticker
    parameters:user_in str
    returns:tickerout str
    """
    search_results=search(user_in)
    op_search_results=[]
    count=0
    #selecting top 5 equity type only search results
    for i in search_results["quotes"]:
        if i["quoteType"]=="EQUITY" and count<5:
            op_search_results.append(i)
            count+=1
    serial=0
    #user output list
    for i in op_search_results:
        serial=serial+1
        print(serial,". ",i["shortname"],"(",i["symbol"],")")
    choice=int(input("Enter the serial no. writen in front of the stock name to track:"))
    
    #print("chosen company=",op_search_results[choice-1]["shortname"],"(",op_search_results[choice-1]["symbol"],")")
    tickerout=op_search_results[choice-1]["symbol"]
    return(tickerout)
    



#TESTING
#name_to_ticker("apple")