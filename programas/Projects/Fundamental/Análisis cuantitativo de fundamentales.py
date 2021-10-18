# For data manipulation
import pandas as pd
# To extract fundamental data
from bs4 import BeautifulSoup
import requests


FALLA EL WEB SCRAPPING... LA PAGINA NO DEJA, DA ERROR 503

#url = ("http://finviz.com/quote.ashx?t=" + symbol.lower())   
url2= ("https://dataquestio.github.io/web-scraping-pages/simple.html")
url =("https://finviz.com/quote.ashx?t=app")


stock_list_ = ['APP','FB','T','TSLA','TWTR','GOOG','AMZN','NET','GE','III','SHOP','NWSA','NFLX','MSFT','CHK','FR','MU','UA','SPY','SES','WORK','NVDA','BRY','TRMD','IBM','FSLY','QCOM','AMBA','NIO','DSX','CTIC','SPCE','CMCSA','CHNG','OHI','BRK-B','FNV','HLF','NWL','FAZ','PACD','SCIF','KHC','TAN','PCG','NVO','ATVI','AMRN','PW','PG','WFC','SCO','TTD','LYB','PBR','FM','GPRO','SLP','OI','QES','ABBV','IBB','FSLR','CBL','AMD','LVS','MPC','CLPS','SALT','BDRY','AMRH','GBR','F','TGA','PHUN','LPL','DMTK','NOK','TEAM','MTP','IBKR','ATRA','AUDC','AT','SND','NETE','SNES','WEAT','JNJ','AOBC','JPM','GOLD','USO','MT','TEUM','BAC','RARX','TUR','STAA','LABU','FCAU','WHLR','XOM','GILD','BRF','PAM','JAG','PRPO','NOA','MVIS','CEE','GS','CBT','SPMD','SPMD','GAIA','STNG','IPG','SSW','UBS','ZIOP','DAL','USAP','KHC','GUT','LMNR','ACHN','IID','KEY','RAD','TRNX','CCJ','PULS','INTC','JJG','KGC','KR','ZNGA','CBAY','NSU','OMP','FINX','PIH','PXD','RDI','SRDX','BVN','DWDP','TWLO','CAMP','USAU','CETX','RDNT','ESI','CXW','HOFT','KODK','CLDT','AAOI','SEDG','RC','IRM','SHW','OPB','AL','VFF','TSN','ACER','BRK-A','XEL','MSN','XLNX','I','AFL','LB','HQL','SCON','GLBS','BBX','CVNA','GRUB','HIIQ','KLIC','VEU','SVXY','AAPL','RL','TK','SHIP','IDT','NEPT','BIF','GNOM','SIVR','RCON','CPAC','TA','VUZI','ZIOP','MPLX','RENN','ZSL','SQM','EWJ','MNRL','SCHG','CHTR','ANF','SPTN','LIVE','NYT','MSFT','ACST','DDD','CO','STON','HSY','CRNT','SAN','MERC','WNC','CENX','PRU','NTNX','PANW','URA','ARKK','HPE','KSS','MNKD','PSEC','DEA','TOPS','EDC','DSX','GLNG','PII','SNE','EZPW','BA','MNST','MDC','VEEV','PFNX','MJ','PFF','VVUS','VOO','IBIO','SDRL','GNW','SLB','FTR','BABA','UVE','BTI','LEDS','DB','ATRI','TTEK','BOND','GEVO','RDN','SBRA','BNO','JAKK','EMR','BHP','CREG','ITRN','AA','CL','ENDP','GURE','JVA','CRESY','SHO','PTH','MFA','FAS','CCMP','IPHS','SPG','NSYS','CTL','CNCE','SEED','GPRO','CMI','NUGT','JKS','AVAV','AWRE','RBBN','CEQP','XXII','GIS','BB','ZEN','UBER','RDFN','PAYX','HEXO','QUAD','SILK','MCK','TCCO','LNT','ISEE','IVERIC','PLX','AEM','YEXT','ALKS','MESO','CBIO','ALXN','ABEO',]
stock_list = ['APP','TSL']

metric = ['P/B','P/E','Forward P/E','PEG','Debt/Eq','Volume','EPS (ttm)','Dividend %','ROE','ROI','EPS Q/Q','Insider Own','52W High','Short Float']


page = requests.get(url2)
print (page)

soup = BeautifulSoup(page.content, 'html.parser')

print(soup.prettify())

print (soup.title)

soup.find_all('some')

soup.find(text = metric).find_next(class_='snapshot-td2').text




df = pd.DataFrame(index=stock_list,columns=metric)
df = get_fundamental_data(df)
print(df.head())

def get_fundamental_data(df):
    for symbol in df.index:
        try:
            #url = ("http://finviz.com/quote.ashx?t=" + symbol.lower())   
            url2= ("https://dataquestio.github.io/web-scraping-pages/simple.html")
            url =("https://finviz.com/quote.ashx?t=app")
            
            
            kk=requests.get(url).content
            page=requests.get(url2)
            
            print(page.status_code)
            
            so__ = BeautifulSoup(page.content, 'html.parser')
                
            print(so__.prettyfy())
            #soup = BeautifulSoup(html_doc, 'html.parser')
            for m in df.columns:                
                df.loc[symbol,m] = fundamental_metric(soup,m)                
        except Exception as e:
            print (symbol, 'not found')
    return df




def fundamental_metric(soup, metric):
    return soup.find(text = metric).find_next(class_='snapshot-td2').text







